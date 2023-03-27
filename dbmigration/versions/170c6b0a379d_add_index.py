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

"""add index

Revision ID: 170c6b0a379d
Revises: 0e75721840ab
Create Date: 2023-03-26 18:12:40.278625

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "170c6b0a379d"
down_revision = "0e75721840ab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("idx_chainmeta_chain"), "chainmeta", ["chain"])
    op.create_index(
        op.f("idx_chainmeta_chain_address"), "chainmeta", ["chain", "address"]
    )
    op.create_index(
        op.f("idx_chainmeta_chain_namespace_scope_tag"),
        "chainmeta",
        ["chain", "namespace", "scope", "tag"],
    )
    op.create_index(op.f("idx_chainmeta_submitted_by"), "chainmeta", ["submitted_by"])


def downgrade() -> None:
    op.drop_index(op.f("idx_chainmeta_chain"), "chainmeta")
    op.drop_index(op.f("idx_chainmeta_chain_address"), "chainmeta")
    op.drop_index(op.f("idx_chainmeta_chain_namespace_scope_tag"), "chainmeta")
    op.drop_index(op.f("idx_chainmeta_submitted_by"), "chainmeta")
