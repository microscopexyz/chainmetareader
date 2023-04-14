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

"""add unique key to avoid duplication

Revision ID: 449a20c2a993
Revises: dac3637b91db
Create Date: 2023-04-12 14:21:12.213115

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "449a20c2a993"
down_revision = "dac3637b91db"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_chainmeta_chain_address_namespace_scope_tag_source_submitted_by"),
        "chainmeta",
        ["chain", "address", "namespace", "scope", "tag", "source", "submitted_by"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_chainmeta_chain_address_namespace_scope_tag_source_submitted_by"),
        "chainmeta",
        "unique",
    )
