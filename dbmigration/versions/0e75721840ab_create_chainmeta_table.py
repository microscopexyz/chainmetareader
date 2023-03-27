# Copyright 2023 The chainmetareader Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""create chainmeta table

Revision ID: 0e75721840ab
Revises: None
Create Date: 2023-03-26 15:12:33.633052

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0e75721840ab"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chainmeta",
        sa.Column("id", sa.Integer()),
        sa.Column("chain", sa.VARCHAR(64), nullable=False),
        sa.Column("address", sa.VARCHAR(256), nullable=False),
        sa.Column("namespace", sa.VARCHAR(64), nullable=False),
        sa.Column("scope", sa.VARCHAR(64), nullable=False),
        sa.Column("tag", sa.VARCHAR(64), nullable=False),
        sa.Column("submitted_by", sa.VARCHAR(64), nullable=False),
        sa.Column("submitted_by", sa.VARCHAR(64), nullable=False),
        sa.Column("submitted_on", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("chainmeta")
