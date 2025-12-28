"""Add index on species.lifespan_years

Revision ID: 997a8b29db79
Revises: 3eb2cb27c3bc
Create Date: 2025-12-28 18:44:42.312570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '997a8b29db79'
down_revision: Union[str, Sequence[str], None] = '3eb2cb27c3bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_species_lifespan_years', 'species', ['lifespan_years'])


def downgrade() -> None:
    op.drop_index('ix_species_lifespan_years', table_name='species')
