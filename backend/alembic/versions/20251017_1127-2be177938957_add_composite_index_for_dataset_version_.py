"""add composite index for dataset version lookups

Revision ID: 2be177938957
Revises: e57dddfd4d2a
Create Date: 2025-10-17 11:27:11.998113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2be177938957'
down_revision: Union[str, None] = 'e57dddfd4d2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add composite index for efficient dataset version lookups.

    This index optimizes queries that fetch the latest version of a dataset
    for a specific tenant, template type, entity, and period.

    Example query:
        SELECT * FROM datasets
        WHERE tenant_id = 1
          AND template_type = 'BankStatement'
          AND entity = 'Main Operating Account'
          AND period_start = '2024-01-01'
        ORDER BY version DESC
        LIMIT 1;
    """
    # Create composite index for dataset version lookups
    op.create_index(
        'ix_dataset_version_lookup',
        'datasets',
        ['tenant_id', 'template_type', 'entity', 'period_start', 'version'],
        unique=False
    )


def downgrade() -> None:
    """Remove composite index for dataset version lookups."""
    op.drop_index('ix_dataset_version_lookup', table_name='datasets')
