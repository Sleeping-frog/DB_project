"""Add conservation_status to species

Revision ID: 3eb2cb27c3bc
Revises: 
Create Date: 2025-12-28 18:37:05.748950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eb2cb27c3bc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('species', sa.Column('conservation_status', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('species', 'conservation_status')
