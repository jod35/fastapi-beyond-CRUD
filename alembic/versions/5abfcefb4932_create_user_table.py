"""create user table

Revision ID: 5abfcefb4932
Revises: 
Create Date: 2024-05-21 01:15:56.346394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5abfcefb4932'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_accounts",
        sa.Column('uid',sa.UUID),
        sa.Column('username',sa.String),
        sa.Column('first_name',sa.String,nullable=False),
        sa.Column('last_name',sa.String,nullable=False),
        sa.Column('is_verified',sa.String,default=True),
        sa.Column('email',sa.String,nullable=False),
        sa.Column('password_hash',sa.String,nullable=False),
        sa.column('created_at',default=sa.func.now)
    )



def downgrade() -> None:
    op.drop_table(
        'user_accounts'
    )