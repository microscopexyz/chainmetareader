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

"""add gmt_create and gmt_modified

Revision ID: e7429574614a
Revises: 449a20c2a993
Create Date: 2024-03-25 16:49:23.941699

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e7429574614a"
down_revision = "449a20c2a993"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "chainmeta",
        sa.Column(
            "gmt_create", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "chainmeta",
        sa.Column(
            "gmt_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(op.f("idx_source"), "chainmeta", ["source"])
    op.create_index(op.f("idx_modified"), "chainmeta", ["gmt_modified"])


def downgrade() -> None:
    op.drop_index(op.f("idx_modified"), "chainmeta")
    op.drop_index(op.f("idx_source"), "chainmeta")
    op.drop_column("chainmeta", "gmt_modified")
    op.drop_column("chainmeta", "gmt_create")
