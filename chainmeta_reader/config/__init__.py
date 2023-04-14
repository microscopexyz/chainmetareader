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

import json
import os
import re
from dataclasses import dataclass
from typing import Set


@dataclass
class KeyedItem:
    key: str
    display_name: str

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, __value: object) -> bool:
        if hasattr(__value, "key"):
            return self.key == __value.key
        else:
            return self.key == __value

    def validate(self):
        """Validate the key, return True if valid, False otherwise"""

        # Key must only contains alphanumeric characters and underscores
        if re.search("[^0-9a-zA-Z_]+", self.key):
            return False

        # Key must be all lowercase
        return self.key == self.key.lower()


@dataclass
class Category(KeyedItem):
    display_name: str
    description: str

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)


@dataclass
class Config:
    Categories: Set[Category]
    Entities: Set[KeyedItem]
    Sources: Set[KeyedItem]
    Chains: Set[KeyedItem]


def validate_config(config: Config):
    """Validate the config, raise ValueError if any of the keys are invalid"""

    for category in config.Categories:
        if not category.validate():
            raise ValueError(f"Invalid category key: {category.key}")

    for entity in config.Entities:
        if not entity.validate():
            raise ValueError(f"Invalid entity key: {entity.key}")

    for source in config.Sources:
        if not source.validate():
            raise ValueError(f"Invalid source key: {source.key}")

    for chain in config.Chains:
        if not chain.validate():
            raise ValueError(f"Invalid chain key: {chain.key}")


def load_config() -> Config:
    """Load the config from the json files"""

    dir_path = os.path.dirname(os.path.realpath(__file__))

    config = Config(
        set(
            Category(i["key"], i["display_name"], i["description"])
            for i in json.load(open(dir_path + "/categories.json"))
        ),
        set(
            KeyedItem(i["key"], i["display_name"])
            for i in json.load(open(dir_path + "/entities.json"))
        ),
        set(
            KeyedItem(i["key"], i["display_name"])
            for i in json.load(open(dir_path + "/sources.json"))
        ),
        set(
            KeyedItem(i["key"], i["display_name"])
            for i in json.load(open(dir_path + "/chains.json"))
        ),
    )

    validate_config(config)
    return config


default_config = load_config()

__all__ = ["Config", "default_config"]
