"""add content column to post table

Revision ID: 8bd06599ef70
Revises: a2de66112e93
Create Date: 2024-06-01 21:10:36.957963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bd06599ef70'
down_revision: Union[str, None] = 'a2de66112e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
