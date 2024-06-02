"""add-image-to-posts

Revision ID: 60ac9e40d1d8
Revises: 3faf1e1cfd86
Create Date: 2024-06-02 02:54:09.507343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60ac9e40d1d8'
down_revision: Union[str, None] = '3faf1e1cfd86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("image", sa.String()))


def downgrade() -> None:
    op.drop_column("posts", "image")
