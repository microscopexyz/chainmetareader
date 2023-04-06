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

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import List

from chainmeta_reader.constants import Namespace
from chainmeta_reader.validator import ValidatorError


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

    # Submitter of the metadata
    submitted_by: str

    # Last updated time
    submitted_on: datetime


class ITranslator(ABC):
    @abstractmethod
    def to_common_schema(raw_metadata) -> List[ChainmetaItem]:
        """Translate to common schema"""
        pass

    @abstractmethod
    def from_common_schema(intermediate_metadata: List[ChainmetaItem]) -> object:
        """Translate from common schema"""
        pass


class CoinbaseTranslator(ITranslator):
    # Note to developer: should try avoid string literal in code (use constant instead);
    # they are used here because these strings (i.e. fields) are enforced by its JSON schema

    def to_common_schema(raw_metadata) -> Iterator[ChainmetaItem]:
        # Translate a Coinbase formatted metadata into the common layer
        address, network, submitted_by, last_updated = (
            raw_metadata["address"],
            Chain(name=raw_metadata["network_name"]),
            raw_metadata["submitted_by"],
            raw_metadata["last_updated"],
        )

        def _build_meta(tag_type: str, tag_value: str):
            return ChainmetaItem(
                address=address,
                chain=network,
                tag=Tag(namespace=Namespace.CoinBase, scope=tag_type, name=tag_value),
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

    def from_common_schema(intermediate_metadata: Iterable[ChainmetaItem]) -> object:
        # Translate from common layer metadata into a Coinbase formatted metadata

        if not intermediate_metadata:
            return
        network_address = set((m.address, m.chain) for m in intermediate_metadata)
        if len(network_address) > 1:
            raise ValidatorError("not all records belong to same address")

        coinbase_metadata = {"categories": []}
        for m in intermediate_metadata:
            if m.tag.namespace != Namespace.CoinBase:
                continue

            coinbase_metadata["address"] = m.address
            coinbase_metadata["network_name"] = m.chain
            coinbase_metadata["submitted_by"] = m.submitted_by
            coinbase_metadata["last_updated"] = m.submitted_on

            if m.tag.scope == "entity":
                coinbase_metadata["entity"] = m.tag.name
            if m.tag.scope == "name":
                coinbase_metadata["name"] = m.tag.name
            if m.tag.scope == "category":
                coinbase_metadata["categories"] += [m.tag.name]

        return coinbase_metadata


class ChaintoolTranslator(ITranslator):
    # Translate a Chaintool formatted metadata into the common layer
    def to_common_schema(raw_metadata) -> Iterator[ChainmetaItem]:
        address, network, submitted_by, last_updated = (
            raw_metadata["address"],
            Chain(name=raw_metadata["chain"]),
            raw_metadata["submitted_by"],
            raw_metadata["tagged_on"],
        )

        def _build_meta(tag_type: str, tag_value: str):
            return ChainmetaItem(
                address=address,
                chain=network,
                tag=Tag(namespace=Namespace.CHAINTOOL, scope=tag_type, name=tag_value),
                submitted_by=submitted_by,
                submitted_on=last_updated,
            )

        def _build_meta_from_field(field: str):
            return _build_meta(tag_type=field, tag_value=raw_metadata[field])

        if "entity" in raw_metadata:
            yield _build_meta_from_field(field="entity")
        if "entity_name" in raw_metadata:
            yield _build_meta_from_field(field="entity_name")
        for category in raw_metadata.get("categories", "").split(","):
            if category:
                yield _build_meta(tag_type="category", tag_value=category)

    def from_common_schema(intermediate_metadata: Iterable[ChainmetaItem]) -> object:
        # Translate from common layer metadata into a Chaintool formatted metadata
        if not intermediate_metadata:
            return
        network_address = set((m.address, m.chain) for m in intermediate_metadata)
        if len(network_address) > 1:
            raise ValidatorError("not all records belong to same address")

        chaintool_metadata = {"categories": ""}
        categories = []
        for m in intermediate_metadata:
            if m.tag.namespace != Namespace.CHAINTOOL:
                continue

            chaintool_metadata["address"] = m.address
            chaintool_metadata["chain"] = m.chain.name
            chaintool_metadata["submitted_by"] = m.submitted_by
            chaintool_metadata["tagged_on"] = m.submitted_on

            if m.tag.scope == "entity":
                chaintool_metadata["entity"] = m.tag.name
            if m.tag.scope == "entity_name":
                chaintool_metadata["entity_name"] = m.tag.name
            if m.tag.scope == "category":
                categories.append(m.tag.name)

        chaintool_metadata["categories"] = ",".join(categories)

        return chaintool_metadata
