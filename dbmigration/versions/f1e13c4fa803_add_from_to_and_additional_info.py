"""add from to and additional info

Revision ID: f1e13c4fa803
Revises: e7429574614a
Create Date: 2024-03-25 17:08:08.491118

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1e13c4fa803"
down_revision = "e7429574614a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "chainmeta",
        sa.Column("from", sa.DateTime, nullable=True, server_default=sa.func.now()),
    )
    op.add_column("chainmeta", sa.Column("to", sa.DateTime, nullable=True))
    op.add_column("chainmeta", sa.Column("metadata", sa.JSON, nullable=True))


def downgrade() -> None:
    op.drop_column("chainmeta", "metadata")
    op.drop_column("chainmeta", "to")
    op.drop_column("chainmeta", "from")
