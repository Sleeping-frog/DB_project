"""Add field extra (JSON) to species

Revision ID: 3dfd4b96e1b3
Revises: 997a8b29db79
Create Date: 2025-12-28 23:41:42.147155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dfd4b96e1b3'
down_revision: Union[str, Sequence[str], None] = '997a8b29db79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "species",
        sa.Column("extra", sa.JSON, nullable=True)
    )
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_species_extra_trgm
        ON species
        USING GIN ((extra ->> 'notes') gin_trgm_ops);
    """)


def downgrade() -> None:
    op.execute("""
        DROP INDEX IF EXISTS idx_species_extra_trgm;
    """)
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
    op.drop_column("species", "extra")