"""added comments logic

Revision ID: dc7ed4160fe6
Revises: 60ac9e40d1d8
Create Date: 2024-06-02 13:36:35.679784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc7ed4160fe6'
down_revision: Union[str, None] = '60ac9e40d1d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table("comments", sa.Column('id', sa.Integer(), primary_key=True, index=True),
                    sa.Column('post_id', sa.Integer(), sa.ForeignKey("posts.id"), nullable=False),
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    op.drop_table("comments")
