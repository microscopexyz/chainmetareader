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
from abc import ABC
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ChainmetaItem:
    """ChainmetaItem is the common schema for all chain metadata items.
    Reference: /chainmeta_reader/schema/artifact_schema.json
    """

    # Chain identification
    chain: str

    # Wallet or contract address
    address: str

    # Entity id of the address
    entity: str

    # name of the address
    name: Optional[str]

    # Category ids of the address
    categories: List[str]

    # Source of the metadata
    source: str

    # Submitter of the metadata
    submitted_by: str

    # Last updated time
    submitted_on: str


class Translator(ABC):
    def to_common_schema(self, raw_metadata) -> ChainmetaItem:
        return ChainmetaItem(**raw_metadata)

    def from_common_schema(self, common_schema_metadata: ChainmetaItem) -> object:
        return common_schema_metadata.__dict__


class ChaintoolTranslator(Translator):
    @staticmethod
    def normalize_key(key: str) -> str:
        return re.sub("[^a-zA-Z0-9_]", "_", key).lower()

    @staticmethod
    def normalize_chain(chain: str) -> str:
        chain = {
            "ETH": "ethereum_mainnet",
            "BTC": "bitcoin_mainnet",
        }.get(chain, chain)

        return ChaintoolTranslator.normalize_key(chain)

    @staticmethod
    def normalize_source(source: str) -> str:
        source = {
            "third party verified": "external",
        }.get(source, source)

        return ChaintoolTranslator.normalize_key(source)

    def to_common_schema(self, raw_metadata: Dict[str, str]) -> ChainmetaItem:
        # Translate Chaintool formatted metadata into the common schema
        return ChainmetaItem(
            chain=ChaintoolTranslator.normalize_chain(raw_metadata["chain"]),
            address=raw_metadata["address"],
            entity=ChaintoolTranslator.normalize_key(raw_metadata["entity"]),
            name=raw_metadata["entity_name"],
            categories=[
                ChaintoolTranslator.normalize_key(i)
                for i in raw_metadata["categories"].split(",")
            ],
            source=ChaintoolTranslator.normalize_source(raw_metadata["source"]),
            submitted_by=raw_metadata["submitted_by"],
            submitted_on=raw_metadata["tagged_on"],
        )

    def from_common_schema(self, common_schema_metadata: ChainmetaItem) -> object:
        # Translate from common schema into Chaintool formatted metadata

        return {
            "chain": common_schema_metadata.chain,
            "address": common_schema_metadata.address,
            "entity": common_schema_metadata.entity,
            "entity_name": common_schema_metadata.name,
            "categories": ",".join(common_schema_metadata.categories),
            "source": common_schema_metadata.source,
            "submitted_by": common_schema_metadata.submitted_by,
            "tagged_on": common_schema_metadata.submitted_on,
        }
