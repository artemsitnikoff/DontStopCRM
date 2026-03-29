from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import Optional
from src.chats.schemas import (
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    MessageFilter,
)
from src.chats.service import ChatService
from src.chats.dependencies import get_chat_service
from src.chats.exceptions import MessageNotFoundException, InvalidLeadException
from src.common.dependencies import get_current_active_user
from src.common.schemas import PaginatedResponse, Pagination, ApiResponse
from src.auth.models import User
from src.chats.constants import MessageSenderType

router = APIRouter(prefix="/api/v1/chats", tags=["chats"])


@router.post("/messages", response_model=MessageResponse, status_code=201)
async def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Create a new message."""
    try:
        message = await chat_service.create_message(message_data)
        return message
    except InvalidLeadException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/messages", response_model=PaginatedResponse[MessageResponse])
async def get_messages(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    lead_id: Optional[int] = None,
    sender_type: Optional[MessageSenderType] = None,
    is_read: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get list of messages with pagination and filters."""
    filters = MessageFilter(
        lead_id=lead_id,
        sender_type=sender_type,
        is_read=is_read
    )
    skip = (page - 1) * size

    messages = await chat_service.get_messages(filters=filters, skip=skip, limit=size)
    total = await chat_service.count_messages(filters=filters)

    pagination = Pagination(
        page=page,
        size=size,
        total=total,
        pages=(total + size - 1) // size if total > 0 else 0
    )

    return PaginatedResponse(
        items=[MessageResponse.model_validate(message) for message in messages],
        pagination=pagination
    )


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get message by ID."""
    message = await chat_service.get_message_by_id(message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with id {message_id} not found"
        )
    return message


@router.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_data: MessageUpdate,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Update message."""
    try:
        updated_message = await chat_service.update_message(message_id, message_data)
        return updated_message
    except MessageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/messages/{message_id}", status_code=204)
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Delete message."""
    try:
        await chat_service.delete_message(message_id)
        return JSONResponse(status_code=204, content=None)
    except MessageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/leads/{lead_id}/mark-read", response_model=ApiResponse[dict])
async def mark_messages_as_read(
    lead_id: int,
    current_user: User = Depends(get_current_active_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    """Mark all messages for a lead as read."""
    count = await chat_service.mark_messages_as_read(lead_id)
    return ApiResponse(
        data={"marked_count": count},
        message=f"Marked {count} messages as read"
    )