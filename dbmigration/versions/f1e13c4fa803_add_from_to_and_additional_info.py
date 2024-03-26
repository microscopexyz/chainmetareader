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

"""add from to and additional info

Revision ID: f1e13c4fa803
Revises: e7429574614a
Create Date: 2024-03-25 17:08:08.491118

"""

import sqlalchemy as sa
from alembic import op

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
