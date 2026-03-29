"""create messages table

Revision ID: 002
Revises: 001
Create Date: 2026-03-29 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types for PostgreSQL
    message_direction_enum = sa.Enum('in', 'out', name='messagedirection')
    message_source_enum = sa.Enum('telegram', 'whatsapp', 'manual', name='messagesource')

    message_direction_enum.create(op.get_bind())
    message_source_enum.create(op.get_bind())

    # Create messages table
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('direction', message_direction_enum, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('source', message_source_enum, nullable=False),
    sa.Column('is_from_agent', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.create_index(op.f('ix_messages_lead_id'), 'messages', ['lead_id'], unique=False)
    op.create_index(op.f('ix_messages_created_at'), 'messages', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_messages_created_at'), table_name='messages')
    op.drop_index(op.f('ix_messages_lead_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')

    # Drop enum types
    sa.Enum(name='messagesource').drop(op.get_bind())
    sa.Enum(name='messagedirection').drop(op.get_bind())