"""add new fields to User

Revision ID: d360a41cc80b
Revises: 5ceb1b2a63bf
Create Date: 2024-07-24 23:13:00.632417

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d360a41cc80b"
down_revision: Union[str, None] = "5ceb1b2a63bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
