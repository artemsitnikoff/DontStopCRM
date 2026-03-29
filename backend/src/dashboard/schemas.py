from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict, List
from src.leads.constants import LeadStatus, LeadSource
from src.calendar.constants import AppointmentType


class LeadStats(BaseModel):
    """Lead statistics schema."""
    total_leads: int
    leads_by_status: Dict[LeadStatus, int]
    leads_by_source: Dict[LeadSource, int]
    new_leads_today: int
    new_leads_this_week: int
    new_leads_this_month: int


class ChatStats(BaseModel):
    """Chat statistics schema."""
    total_messages: int
    unread_messages: int
    messages_today: int
    messages_this_week: int
    active_conversations: int


class CalendarStats(BaseModel):
    """Calendar statistics schema."""
    total_appointments: int
    appointments_by_type: Dict[AppointmentType, int]
    appointments_today: int
    appointments_this_week: int
    upcoming_appointments: int


class ActivityItem(BaseModel):
    """Recent activity item schema."""
    id: int
    type: str  # "lead_created", "message_sent", "appointment_scheduled"
    title: str
    description: str
    timestamp: datetime
    related_id: int  # lead_id, message_id, appointment_id


class DashboardResponse(BaseModel):
    """Dashboard response schema."""
    lead_stats: LeadStats
    chat_stats: ChatStats
    calendar_stats: CalendarStats
    recent_activity: List[ActivityItem]
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)