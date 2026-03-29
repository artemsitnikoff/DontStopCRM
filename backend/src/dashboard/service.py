from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from datetime import datetime, timedelta
from typing import Dict, List
from src.leads.models import Lead
from src.chats.models import Message
from src.calendar.models import Appointment
from src.dashboard.schemas import (
    LeadStats,
    ChatStats,
    CalendarStats,
    ActivityItem,
    DashboardResponse
)
from src.leads.constants import LeadStatus, LeadSource
from src.calendar.constants import AppointmentType
from src.chats.constants import MessageSenderType


class DashboardService:
    """Dashboard service for aggregating statistics."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_lead_stats(self) -> LeadStats:
        """Get lead statistics."""
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Total leads
        total_result = await self.db.execute(select(func.count(Lead.id)))
        total_leads = total_result.scalar()

        # Leads by status
        status_result = await self.db.execute(
            select(Lead.status, func.count(Lead.id))
            .group_by(Lead.status)
        )
        leads_by_status = {status: count for status, count in status_result.all()}

        # Fill missing statuses with 0
        for status in LeadStatus:
            if status not in leads_by_status:
                leads_by_status[status] = 0

        # Leads by source
        source_result = await self.db.execute(
            select(Lead.source, func.count(Lead.id))
            .group_by(Lead.source)
        )
        leads_by_source = {source: count for source, count in source_result.all()}

        # Fill missing sources with 0
        for source in LeadSource:
            if source not in leads_by_source:
                leads_by_source[source] = 0

        # New leads today
        today_result = await self.db.execute(
            select(func.count(Lead.id))
            .where(Lead.created_at >= today_start)
        )
        new_leads_today = today_result.scalar()

        # New leads this week
        week_result = await self.db.execute(
            select(func.count(Lead.id))
            .where(Lead.created_at >= week_start)
        )
        new_leads_this_week = week_result.scalar()

        # New leads this month
        month_result = await self.db.execute(
            select(func.count(Lead.id))
            .where(Lead.created_at >= month_start)
        )
        new_leads_this_month = month_result.scalar()

        return LeadStats(
            total_leads=total_leads,
            leads_by_status=leads_by_status,
            leads_by_source=leads_by_source,
            new_leads_today=new_leads_today,
            new_leads_this_week=new_leads_this_week,
            new_leads_this_month=new_leads_this_month,
        )

    async def get_chat_stats(self) -> ChatStats:
        """Get chat statistics."""
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())

        # Total messages
        total_result = await self.db.execute(select(func.count(Message.id)))
        total_messages = total_result.scalar()

        # Unread messages
        unread_result = await self.db.execute(
            select(func.count(Message.id))
            .where(Message.is_read == False)
        )
        unread_messages = unread_result.scalar()

        # Messages today
        today_result = await self.db.execute(
            select(func.count(Message.id))
            .where(Message.created_at >= today_start)
        )
        messages_today = today_result.scalar()

        # Messages this week
        week_result = await self.db.execute(
            select(func.count(Message.id))
            .where(Message.created_at >= week_start)
        )
        messages_this_week = week_result.scalar()

        # Active conversations (leads with messages in last 7 days)
        active_result = await self.db.execute(
            select(func.count(func.distinct(Message.lead_id)))
            .where(Message.created_at >= week_start)
        )
        active_conversations = active_result.scalar()

        return ChatStats(
            total_messages=total_messages,
            unread_messages=unread_messages,
            messages_today=messages_today,
            messages_this_week=messages_this_week,
            active_conversations=active_conversations,
        )

    async def get_calendar_stats(self) -> CalendarStats:
        """Get calendar statistics."""
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        week_start = today_start - timedelta(days=today_start.weekday())
        week_end = week_start + timedelta(days=7)

        # Total appointments
        total_result = await self.db.execute(select(func.count(Appointment.id)))
        total_appointments = total_result.scalar()

        # Appointments by type
        type_result = await self.db.execute(
            select(Appointment.type, func.count(Appointment.id))
            .group_by(Appointment.type)
        )
        appointments_by_type = {type_: count for type_, count in type_result.all()}

        # Fill missing types with 0
        for type_ in AppointmentType:
            if type_ not in appointments_by_type:
                appointments_by_type[type_] = 0

        # Appointments today
        today_result = await self.db.execute(
            select(func.count(Appointment.id))
            .where(
                and_(
                    Appointment.start_time >= today_start,
                    Appointment.start_time < today_end
                )
            )
        )
        appointments_today = today_result.scalar()

        # Appointments this week
        week_result = await self.db.execute(
            select(func.count(Appointment.id))
            .where(
                and_(
                    Appointment.start_time >= week_start,
                    Appointment.start_time < week_end
                )
            )
        )
        appointments_this_week = week_result.scalar()

        # Upcoming appointments (from now)
        upcoming_result = await self.db.execute(
            select(func.count(Appointment.id))
            .where(Appointment.start_time > now)
        )
        upcoming_appointments = upcoming_result.scalar()

        return CalendarStats(
            total_appointments=total_appointments,
            appointments_by_type=appointments_by_type,
            appointments_today=appointments_today,
            appointments_this_week=appointments_this_week,
            upcoming_appointments=upcoming_appointments,
        )

    async def get_recent_activity(self, limit: int = 10) -> List[ActivityItem]:
        """Get recent activity across all modules."""
        activities = []

        # Recent leads
        leads_result = await self.db.execute(
            select(Lead)
            .order_by(desc(Lead.created_at))
            .limit(limit // 3)
        )
        for lead in leads_result.scalars():
            activities.append(ActivityItem(
                id=len(activities) + 1,
                type="lead_created",
                title="New Lead Created",
                description=f"Lead '{lead.name}' was created",
                timestamp=lead.created_at,
                related_id=lead.id,
            ))

        # Recent messages
        messages_result = await self.db.execute(
            select(Message)
            .order_by(desc(Message.created_at))
            .limit(limit // 3)
        )
        for message in messages_result.scalars():
            sender = "Client" if message.sender_type == MessageSenderType.CLIENT else "Agent"
            activities.append(ActivityItem(
                id=len(activities) + 1,
                type="message_sent",
                title=f"Message from {sender}",
                description=f"New message in lead conversation",
                timestamp=message.created_at,
                related_id=message.id,
            ))

        # Recent appointments
        appointments_result = await self.db.execute(
            select(Appointment)
            .order_by(desc(Appointment.created_at))
            .limit(limit // 3)
        )
        for appointment in appointments_result.scalars():
            activities.append(ActivityItem(
                id=len(activities) + 1,
                type="appointment_scheduled",
                title="Appointment Scheduled",
                description=f"'{appointment.title}' scheduled",
                timestamp=appointment.created_at,
                related_id=appointment.id,
            ))

        # Sort by timestamp and limit
        activities.sort(key=lambda x: x.timestamp, reverse=True)
        return activities[:limit]

    async def get_dashboard_data(self) -> DashboardResponse:
        """Get complete dashboard data."""
        lead_stats = await self.get_lead_stats()
        chat_stats = await self.get_chat_stats()
        calendar_stats = await self.get_calendar_stats()
        recent_activity = await self.get_recent_activity()

        return DashboardResponse(
            lead_stats=lead_stats,
            chat_stats=chat_stats,
            calendar_stats=calendar_stats,
            recent_activity=recent_activity,
            generated_at=datetime.utcnow(),
        )