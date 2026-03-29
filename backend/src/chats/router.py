from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
import json
import logging
import pydantic
from src.chats.schemas import (
    MessageCreate,
    MessageResponse,
    ChatListResponse,
    MessageListResponse,
)
from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service
from src.chats.constants import DEFAULT_CHAT_PAGE_SIZE
from src.chats.ws_manager import manager
from src.common.schemas import Pagination
from src.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chats", tags=["chats"])


@router.get("/", response_model=ChatListResponse)
async def get_chats(
    service: ChatService = Depends(get_chat_service),
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
    message_data: MessageCreate,
    service: ChatService = Depends(get_chat_service),
):
    """Send a message to a lead."""
    # Override lead_id from path
    message_data.lead_id = lead_id
    message = await service.create_message(message_data)

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
    await manager.connect(websocket, lead_id)
    try:
        while True:
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON"
                }))
                continue

            try:
                # Validate message data
                create_data = MessageCreate(**message_data)
                create_data.lead_id = lead_id
            except pydantic.ValidationError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid message format"
                }))
                continue

            # Create database session and service
            async with AsyncSessionLocal() as db:
                service = ChatService(db)

                # Create message through service
                message = await service.create_message(create_data)

                # Broadcast to all connections for this lead
                message_dict = {
                    "type": "message",
                    "data": MessageResponse.model_validate(message).model_dump(mode='json')
                }
                await manager.send_message(message_dict, lead_id)

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