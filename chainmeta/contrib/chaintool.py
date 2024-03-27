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

import re
from pathlib import Path
from typing import Dict, Optional

from chainmeta.metadata import ChainmetaItem, ITranslator
from chainmeta.validator import JsonValidator


class ChaintoolTranslator(ITranslator):
    @staticmethod
    def normalize_not_none_key(key: str) -> str:
        return re.sub("[^a-zA-Z0-9_]", "_", key).lower()

    @staticmethod
    def normalize_key(key: str) -> Optional[str]:
        if key is None:
            return None
        return ChaintoolTranslator.normalize_not_none_key(key)

    @staticmethod
    def normalize_chain(chain: str) -> str:
        return {
            "ETH": "ethereum_mainnet",
            "BTC": "bitcoin_mainnet",
        }.get(chain, chain)

    @staticmethod
    def denormalize_chain(chain: str) -> str:
        return {
            "ethereum_mainnet": "ETH",
            "bitcoin_mainnet": "BTC",
        }.get(chain, chain)

    @staticmethod
    def normalize_category(category: str) -> str:
        category = {
            "Financial Services": "business_or_services",
            "Services": "business_or_services",
            "Exchange": "cex",
            "Law Enforcement": "le",
            "Coinswapper": "coin_swapper",
            "Financial Crime": "financial_crime",
            "Constrainted": "constrained_by_service",
            "High Risk": "high_risk",
            "Dapp": "dapp",
        }.get(category, category)

        return ChaintoolTranslator.normalize_not_none_key(category)

    @staticmethod
    def denormalize_category(category: str) -> str:
        return {
            "business_or_services": "Services",
            "cex": "Exchange",
            "le": "Law Enforcement",
            "coin_swapper": "Coinswapper",
            "financial_crime": "Financial Crime",
            "constrained_by_service": "Constrainted",
            "high_risk": "High Risk",
            "dapp": "Dapp",
        }.get(category, category)

    def to_common_schema(self, raw_metadata: Dict[str, str]) -> Optional[ChainmetaItem]:
        # Translate Chaintool formatted metadata into the common schema
        return ChainmetaItem(
            chain=ChaintoolTranslator.normalize_chain(raw_metadata["chain"]),
            address=raw_metadata["address"],
            entity=ChaintoolTranslator.normalize_key(raw_metadata["entity"]),
            name=raw_metadata["entity_name"],
            categories=[
                ChaintoolTranslator.normalize_category(i)
                for i in raw_metadata["categories"].split(",")
            ],
            source=ChaintoolTranslator.normalize_not_none_key(raw_metadata["source"]),
            submitted_by=raw_metadata["submitted_by"],
            submitted_on=raw_metadata["tagged_on"],
            additional_metadata={},
        )

    def from_common_schema(
        self, common_schema_metadata: ChainmetaItem
    ) -> Optional[object]:
        # Translate from common schema into Chaintool formatted metadata

        return {
            "chain": ChaintoolTranslator.denormalize_chain(
                common_schema_metadata.chain
            ),
            "address": common_schema_metadata.address,
            "entity": common_schema_metadata.entity,
            "entity_name": common_schema_metadata.name,
            "categories": ",".join(
                [
                    ChaintoolTranslator.denormalize_category(i)
                    for i in common_schema_metadata.categories
                ]
            ),
            "source": common_schema_metadata.source,
            "submitted_by": common_schema_metadata.submitted_by,
            "tagged_on": common_schema_metadata.submitted_on,
        }


schema_path = [
    "https://github.com/openchainmeta/chainmetareader/chainmeta/schemas/chaintool_schema.json"  # noqa: E501
]

validator = JsonValidator(
    schema=Path(__file__).parent.resolve().joinpath("chaintool_schema.json")
)
translator = ChaintoolTranslator()
