"""create events table

Revision ID: 003_create_events_table
Revises: 002_create_messages_table
Create Date: 2026-03-29

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_create_events_table'
down_revision = '002_create_messages_table'
branch_labels = None
depends_on = None


def upgrade():
    # Create enum types
    event_type_enum = sa.Enum('booking', 'task', 'follow_up', name='eventtype')
    event_status_enum = sa.Enum('planned', 'done', 'cancelled', name='eventstatus')

    event_type_enum.create(op.get_bind())
    event_status_enum.create(op.get_bind())

    # Create events table
    op.create_table('events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('lead_id', sa.Integer(), nullable=True),
        sa.Column('event_type', event_type_enum, nullable=False),
        sa.Column('status', event_status_enum, nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_events_id', 'events', ['id'], unique=False)
    op.create_index('ix_events_start_at', 'events', ['start_at'], unique=False)
    op.create_index('ix_events_lead_id', 'events', ['lead_id'], unique=False)
    op.create_index('ix_events_start_at_lead_id', 'events', ['start_at', 'lead_id'], unique=False)
    op.create_index('ix_events_event_type_status', 'events', ['event_type', 'status'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_events_event_type_status', table_name='events')
    op.drop_index('ix_events_start_at_lead_id', table_name='events')
    op.drop_index('ix_events_lead_id', table_name='events')
    op.drop_index('ix_events_start_at', table_name='events')
    op.drop_index('ix_events_id', table_name='events')

    # Drop table
    op.drop_table('events')

    # Drop enum types
    sa.Enum(name='eventstatus').drop(op.get_bind())
    sa.Enum(name='eventtype').drop(op.get_bind())