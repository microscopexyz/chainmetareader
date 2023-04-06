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
from dataclasses import dataclass
from datetime import datetime
from typing import List

from chainmeta_reader.constants import Namespace
from chainmeta_reader.validator import ValidatorError, common_artifact_validator


@dataclass(eq=True, frozen=True)
class Chain:
    """Chain represents a uniquely identified blockchain,
    e.g. ethereum mainnet, or ethereum goerli
    """

    # The string representation of the network
    name: str


@dataclass(eq=True, frozen=True)
class Tag:
    """Tag is a generic container for any information like name,
    entity or category etc.
    """

    # Namespace this tag belongs to
    namespace: Namespace

    # Scope of the tag, e.g. entity, category or attribute
    scope: str

    # The string representation of the tag
    name: str


@dataclass
class ChainmetaItem:
    """Intermediate representation of the metadata."""

    # Chain identification
    chain: Chain

    # Wallet or contract address
    address: str

    # Single piece of metadata
    tag: Tag

    # Source of the metadata
    source: str

    # Submitter of the metadata
    submitted_by: str

    # Last updated time
    submitted_on: datetime


class Translator:
    def to_common_schema(self, raw_metadata) -> List[ChainmetaItem]:
        common_artifact_validator.validate([raw_metadata])

        address, network, source, submitted_by, last_updated = (
            raw_metadata["address"],
            Chain(name=raw_metadata["chain"]),
            raw_metadata["source"],
            raw_metadata["submitted_by"],
            raw_metadata["submitted_on"],
        )

        def _build_meta(tag_type: str, tag_value: str):
            return ChainmetaItem(
                address=address,
                chain=network,
                tag=Tag(namespace=Namespace.GLOBAL, scope=tag_type, name=tag_value),
                source=source,
                submitted_by=submitted_by,
                submitted_on=last_updated,
            )

        def _build_meta_from_field(field: str):
            return _build_meta(tag_type=field, tag_value=raw_metadata[field])

        if "entity" in raw_metadata:
            yield _build_meta_from_field(field="entity")
        if "name" in raw_metadata:
            yield _build_meta_from_field(field="name")
        for category in raw_metadata.get("categories", []):
            yield _build_meta(tag_type="category", tag_value=category)

    def from_common_schema(self, common_schema_metadata: List[ChainmetaItem]) -> object:
        if not common_schema_metadata:
            return
        network_address = set((m.address, m.chain) for m in common_schema_metadata)
        if len(network_address) > 1:
            raise ValidatorError("not all records belong to same address")

        raw_metadata = {"categories": []}
        for m in common_schema_metadata:
            if m.tag.namespace != Namespace.GLOBAL:
                continue

            raw_metadata["chain"] = m.chain
            raw_metadata["address"] = m.address
            raw_metadata["source"] = m.source
            raw_metadata["submitted_by"] = m.submitted_by
            raw_metadata["submitted_on"] = m.submitted_on

            if m.tag.scope == "entity":
                raw_metadata["entity"] = m.tag.name
            if m.tag.scope == "name":
                raw_metadata["name"] = m.tag.name
            if m.tag.scope == "category":
                raw_metadata["categories"] += [m.tag.name]

        return raw_metadata


class ChaintoolTranslator(Translator):
    def normalize_key(key: str) -> str:
        return re.sub("[^a-zA-Z0-9_]", "_", key).lower()

    def normalize_chain(chain: str) -> str:
        chain = {
            "ETH": "ethereum_mainnet",
            "BTC": "bitcoin_mainnet",
        }.get(chain, chain)

        return ChaintoolTranslator.normalize_key(chain)

    def normalize_source(source: str) -> str:
        source = {
            "third party verified": "external",
        }.get(source, source)

        return ChaintoolTranslator.normalize_key(source)

    def to_common_schema(self, raw_metadata: object) -> List[ChainmetaItem]:
        # Translate Chaintool formatted metadata into the common schema
        intermediate = {
            "chain": ChaintoolTranslator.normalize_chain(raw_metadata["chain"]),
            "address": raw_metadata["address"],
            "entity": ChaintoolTranslator.normalize_key(raw_metadata["entity"]),
            "name": raw_metadata["entity_name"],
            "categories": [
                ChaintoolTranslator.normalize_key(i)
                for i in raw_metadata["categories"].split(",")
            ],
            "source": ChaintoolTranslator.normalize_source(raw_metadata["source"]),
            "submitted_by": raw_metadata["submitted_by"],
            "submitted_on": raw_metadata["tagged_on"],
        }

        return super().to_common_schema(intermediate)

    def from_common_schema(
        self,
        common_schema_metadata: List[ChainmetaItem],
    ) -> object:
        # Translate from common schema into Chaintool formatted metadata

        intermediate = super().from_common_schema(common_schema_metadata)
        return {
            "chain": intermediate["chain"].name,
            "address": intermediate["address"],
            "entity": intermediate["entity"],
            "entity_name": intermediate["name"],
            "categories": ",".join(intermediate["categories"]),
            "source": intermediate["source"],
            "submitted_by": intermediate["submitted_by"],
            "tagged_on": intermediate["submitted_on"],
        }
