from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import json
from typing import Dict
from src.chats.schemas import (
    MessageCreate,
    MessageResponse,
    ChatListResponse,
    MessageListResponse,
)
from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service
from src.chats.constants import DEFAULT_CHAT_PAGE_SIZE
from src.common.schemas import Pagination

router = APIRouter(prefix="/api/v1/chats", tags=["chats"])


# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lead_id: int):
        await websocket.accept()
        if lead_id not in self.active_connections:
            self.active_connections[lead_id] = []
        self.active_connections[lead_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lead_id: int):
        if lead_id in self.active_connections:
            self.active_connections[lead_id].remove(websocket)
            if not self.active_connections[lead_id]:
                del self.active_connections[lead_id]

    async def send_message(self, message: dict, lead_id: int):
        if lead_id in self.active_connections:
            connections = self.active_connections[lead_id].copy()
            for connection in connections:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    # Remove disconnected connections
                    self.disconnect(connection, lead_id)


manager = ConnectionManager()


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
        "data": MessageResponse.model_validate(message).model_dump()
    }
    await manager.send_message(message_dict, lead_id)

    return MessageResponse.model_validate(message)


@router.websocket("/ws/{lead_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    lead_id: int,
):
    """WebSocket endpoint for real-time messaging."""
    from src.core.database import AsyncSessionLocal

    await manager.connect(websocket, lead_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Create database session and service
            async with AsyncSessionLocal() as db:
                service = ChatService(db)

                # Create message through service
                create_data = MessageCreate(**message_data)
                create_data.lead_id = lead_id
                message = await service.create_message(create_data)

                # Broadcast to all connections for this lead
                message_dict = {
                    "type": "message",
                    "data": MessageResponse.model_validate(message).model_dump()
                }
                await manager.send_message(message_dict, lead_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, lead_id)
    except Exception as e:
        # Send error message and disconnect
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))
        manager.disconnect(websocket, lead_id)