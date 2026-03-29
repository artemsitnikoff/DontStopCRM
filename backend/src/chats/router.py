from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
import json
import logging
from pydantic import ValidationError
from src.chats.schemas import (
    MessageCreate,
    MessageCreateBody,
    MessageResponse,
    ChatListResponse,
    MessageListResponse,
)
from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service
from src.chats.exceptions import ChatNotFound
from src.chats.constants import DEFAULT_CHAT_PAGE_SIZE
from src.chats.ws_manager import manager
from src.common.schemas import Pagination
from src.core.database import AsyncSessionLocal
from src.common.dependencies import get_current_active_user
from src.auth.models import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chats", tags=["chats"])


async def _process_ws_message(data: str, lead_id: int, websocket: WebSocket):
    """Process a WebSocket message and return response or None if successful."""
    try:
        message_data = json.loads(data)
    except json.JSONDecodeError:
        return {"type": "error", "message": "Invalid JSON"}

    try:
        # Validate message data without lead_id
        body_data = MessageCreateBody(**message_data)
        # Create MessageCreate with lead_id
        create_data = MessageCreate(**body_data.model_dump(), lead_id=lead_id)
    except ValidationError:
        return {"type": "error", "message": "Invalid message format"}

    # Create database session and service
    async with AsyncSessionLocal() as db:
        service = ChatService(db)

        try:
            # Create message through service
            message = await service.create_message(create_data)

            # Broadcast to all connections for this lead
            message_dict = {
                "type": "message",
                "data": MessageResponse.model_validate(message).model_dump(mode='json')
            }
            await manager.send_message(message_dict, lead_id)
            return None  # Success

        except ChatNotFound as e:
            return {"type": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"WS error: {e}")
            return {"type": "error", "message": "Internal error"}


@router.get("/", response_model=ChatListResponse)
async def get_chats(
    service: ChatService = Depends(get_chat_service),
    current_user: User = Depends(get_current_active_user),
):
    """Get list of chat previews grouped by lead."""
    chat_previews = await service.get_chats()
    return ChatListResponse(items=chat_previews)


@router.get("/{lead_id}/messages", response_model=MessageListResponse)
async def get_messages(
    lead_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(DEFAULT_CHAT_PAGE_SIZE, ge=1, le=100),
    service: ChatService = Depends(get_chat_service),
    current_user: User = Depends(get_current_active_user),
):
    """Get message history for a specific lead with pagination."""
    messages, total = await service.get_messages(lead_id, page, size)
    return MessageListResponse(
        items=[MessageResponse.model_validate(message) for message in messages],
        pagination=Pagination(
            page=page,
            size=size,
            total=total,
            pages=(total + size - 1) // size
        )
    )


@router.post("/{lead_id}/messages", response_model=MessageResponse, status_code=201)
async def send_message(
    lead_id: int,
    message_data: MessageCreateBody,
    service: ChatService = Depends(get_chat_service),
    current_user: User = Depends(get_current_active_user),
):
    """Send a message to a lead."""
    # Create MessageCreate with lead_id from path
    create_data = MessageCreate(**message_data.model_dump(), lead_id=lead_id)
    message = await service.create_message(create_data)

    # Broadcast to WebSocket connections
    message_dict = {
        "type": "message",
        "data": MessageResponse.model_validate(message).model_dump(mode='json')
    }
    await manager.send_message(message_dict, lead_id)

    return MessageResponse.model_validate(message)


@router.websocket("/ws/{lead_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    lead_id: int,
):
    """WebSocket endpoint for real-time messaging."""
    # Get token from query params
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Missing token")
        return

    try:
        from src.core.security import verify_token
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            await websocket.close(code=4001, reason="Invalid token")
            return
    except Exception:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await manager.connect(websocket, lead_id)
    try:
        while True:
            data = await websocket.receive_text()
            error_response = await _process_ws_message(data, lead_id, websocket)

            if error_response:
                await websocket.send_text(json.dumps(error_response))
                continue

    except WebSocketDisconnect:
        manager.disconnect(websocket, lead_id)
    except Exception as e:
        # Log actual error details
        logger.error(f"WebSocket error for lead {lead_id}: {e}")

        # Send generic error message to client
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Internal error"
            }))
        except Exception:
            pass  # Connection might already be closed

        manager.disconnect(websocket, lead_id)