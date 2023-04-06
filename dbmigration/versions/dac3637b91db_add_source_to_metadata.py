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

"""add source to metadata

Revision ID: dac3637b91db
Revises: 170c6b0a379d
Create Date: 2023-04-06 00:04:54.158753

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dac3637b91db"
down_revision = "170c6b0a379d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("chainmeta", sa.Column("source", sa.VARCHAR(64), nullable=False))


def downgrade() -> None:
    op.drop_column("chainmeta", "source")
