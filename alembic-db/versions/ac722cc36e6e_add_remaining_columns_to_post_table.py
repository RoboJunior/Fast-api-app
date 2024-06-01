"""add remaining columns to post table

Revision ID: ac722cc36e6e
Revises: 2f307460c342
Create Date: 2024-06-01 22:07:19.190099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ac722cc36e6e'
down_revision: Union[str, None] = '2f307460c342'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published',sa.Boolean(), server_default="TRUE", nullable=False),)
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
