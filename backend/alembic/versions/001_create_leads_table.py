"""create leads table

Revision ID: 001
Revises:
Create Date: 2026-03-29 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types for PostgreSQL
    lead_source_enum = sa.Enum('telegram', 'whatsapp', 'instagram', 'phone', name='leadsource')
    lead_status_enum = sa.Enum('new', 'contacted', 'qualified', 'won', name='leadstatus')

    lead_source_enum.create(op.get_bind())
    lead_status_enum.create(op.get_bind())

    # Create leads table
    op.create_table('leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('source', lead_source_enum, nullable=False),
    sa.Column('status', lead_status_enum, nullable=False),
    sa.Column('first_message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leads_id'), 'leads', ['id'], unique=False)
    op.create_index(op.f('ix_leads_status'), 'leads', ['status'], unique=False)
    op.create_index(op.f('ix_leads_source'), 'leads', ['source'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_leads_source'), table_name='leads')
    op.drop_index(op.f('ix_leads_status'), table_name='leads')
    op.drop_index(op.f('ix_leads_id'), table_name='leads')
    op.drop_table('leads')

    # Drop enum types
    sa.Enum(name='leadstatus').drop(op.get_bind())
    sa.Enum(name='leadsource').drop(op.get_bind())