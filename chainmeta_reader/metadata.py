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
from enum import Enum
from typing import List

from chainmeta_reader.constants import ValidatorType
from chainmeta_reader.validator import ValidatorError


class Namespace(Enum):
    ChainTool = 1
    Coinbase = 2
    GoPlus = 3


@dataclass(eq=True, frozen=True)
class Network:
    """Network represents a uniquely identified blockchain network,
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

    # Type of the tag, e.g. entity, category or attribute
    type: str

    # The string representation of the tag
    name: str


@dataclass
class MetadataItem:
    """Intermediate representation of the metadata."""

    # Wallet or contract address
    address: str

    # Network identification
    network: Network

    # Single piece of metadata
    tag: Tag

    # Submitter of the metadata
    submitted_by: str

    # Last updated time
    last_updated: datetime


class ITranslator(ABC):
    @abstractmethod
    def to_intermediate(raw_metadata) -> List[MetadataItem]:
        """Translate to intermediate representation"""
        pass

    @abstractmethod
    def from_intermediate(intermediate_metadata: List[MetadataItem]) -> object:
        """Translate from intermediate representation"""
        pass


class CoinbaseTranslator(ITranslator):
    # Note to developer: should try avoid string literal in code (use constant instead);
    # they are used here because these strings (i.e. fields) are enforced by its JSON schema

    def to_intermediate(raw_metadata) -> Iterator[MetadataItem]:
        # Translate a Coinbase formatted metadata into the common layer
        address, network, submitted_by, last_updated = (
            raw_metadata["address"],
            Network(name=raw_metadata["network_name"]),
            raw_metadata["submitted_by"],
            raw_metadata["last_updated"],
        )

        def _build_meta(tag_type: str, tag_value: str):
            return MetadataItem(
                address=address,
                network=network,
                tag=Tag(
                    namespace=ValidatorType.CoinBase, type=tag_type, name=tag_value
                ),
                submitted_by=submitted_by,
                last_updated=last_updated,
            )

        def _build_meta_from_field(field: str):
            return _build_meta(tag_type=field, tag_value=raw_metadata[field])

        if "entity" in raw_metadata:
            yield _build_meta_from_field(field="entity")
        if "name" in raw_metadata:
            yield _build_meta_from_field(field="name")
        for category in raw_metadata.get("categories", []):
            yield _build_meta(tag_type="category", tag_value=category)

    def from_intermediate(intermediate_metadata: Iterable[MetadataItem]) -> object:
        # Translate from common layer metadata into a Coinbase formatted metadata

        if not intermediate_metadata:
            return
        network_address = set((m.address, m.network) for m in intermediate_metadata)
        if len(network_address) > 1:
            raise ValidatorError("not all records belong to same address")

        coinbase_metadata = {"categories": []}
        for m in intermediate_metadata:
            if m.tag.namespace != ValidatorType.CoinBase:
                continue

            coinbase_metadata["address"] = m.address
            coinbase_metadata["network_name"] = m.network
            coinbase_metadata["submitted_by"] = m.submitted_by
            coinbase_metadata["last_updated"] = m.last_updated

            if m.tag.type == "entity":
                coinbase_metadata["entity"] = m.tag.name
            if m.tag.type == "name":
                coinbase_metadata["name"] = m.tag.name
            if m.tag.type == "category":
                coinbase_metadata["categories"] += [m.tag.name]

        return coinbase_metadata


class ChaintoolTranslator(ITranslator):
    # Translate a Chaintool formatted metadata into the common layer
    def to_intermediate(raw_metadata) -> Iterator[MetadataItem]:
        address, network, submitted_by, last_updated = (
            raw_metadata["address"],
            Network(name=raw_metadata["chain"]),
            raw_metadata["submitted_by"],
            raw_metadata["tagged_on"],
        )

        def _build_meta(tag_type: str, tag_value: str):
            return MetadataItem(
                address=address,
                network=network,
                tag=Tag(
                    namespace=ValidatorType.ChainTool, type=tag_type, name=tag_value
                ),
                submitted_by=submitted_by,
                last_updated=last_updated,
            )

        def _build_meta_from_field(field: str):
            return _build_meta(tag_type=field, tag_value=raw_metadata[field])

        if "entity_name" in raw_metadata:
            yield _build_meta_from_field(field="entity_name")
        if "name" in raw_metadata:
            yield _build_meta_from_field(field="name")
        for category in raw_metadata.get("categories", "").split(","):
            if category:
                yield _build_meta(tag_type="category", tag_value=category)
        for attribute in raw_metadata.get("attributes", "").split(","):
            if attribute:
                yield _build_meta(tag_type="attribute", tag_value=attribute)

    def from_intermediate(intermediate_metadata: Iterable[MetadataItem]) -> object:
        # Translate from common layer metadata into a Chaintool formatted metadata
        if not intermediate_metadata:
            return
        network_address = set((m.address, m.network) for m in intermediate_metadata)
        if len(network_address) > 1:
            raise ValidatorError("not all records belong to same address")

        chaintool_metadata = {"categories": "", "attributes": ""}
        categories = []
        attributes = []
        for m in intermediate_metadata:
            if m.tag.namespace != ValidatorType.ChainTool:
                continue

            chaintool_metadata["address"] = m.address
            chaintool_metadata["chain"] = m.network.name
            chaintool_metadata["submitted_by"] = m.submitted_by
            chaintool_metadata["tagged_on"] = m.last_updated

            if m.tag.type == "entity_name":
                chaintool_metadata["entity_name"] = m.tag.name
            if m.tag.type == "name":
                chaintool_metadata["name"] = m.tag.name
            if m.tag.type == "category":
                categories.append(m.tag.name)
            if m.tag.type == "attribute":
                attributes.append(m.tag.name)

        chaintool_metadata["categories"] = ",".join(categories)
        chaintool_metadata["attributes"] += ",".join(attributes)

        return chaintool_metadata
