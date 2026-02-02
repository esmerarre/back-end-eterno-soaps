"""add admin table

Revision ID: 9588004b9a11
Revises: 9310513b4350
Create Date: 2026-02-02 11:12:56.092512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9588004b9a11'
down_revision: Union[str, Sequence[str], None] = '9310513b4350'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'admins',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table('admins')
