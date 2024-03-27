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

import importlib
import os
from pathlib import Path
from typing import Dict, Optional

from chainmeta.constants import ContribFolder
from chainmeta.logger import logger
from chainmeta.metadata import ITranslator, Translator
from chainmeta.validator import IValidator, common_artifact_validator


class Schema:
    validator: IValidator
    translator: ITranslator

    def __init__(self, validator: IValidator, translator: ITranslator):
        self.validator = validator
        self.translator = translator


schema_registry: Dict[str, Schema] = {}


def resolve(schema_path: str) -> Optional[Schema]:
    """Resolve a schema by path."""

    return schema_registry.get(schema_path)


def register(schema_path: str, schema: Schema):
    """Register a schema."""

    global schema_registry
    if schema_path in schema_registry:
        raise ValueError(f"Schema {schema_path} already exists")
    schema_registry[schema_path] = schema


common_schema = Schema(common_artifact_validator, Translator())
register(
    "https://github.com/openchainmeta/chainmetareader/chainmeta/schemas/artifact_schema.json",  # noqa: E501
    common_schema,
)
register(
    "https://github.com/openchainmeta/chainmetareader/chainmeta/schema/artifact_schema.json",  # noqa: E501
    common_schema,
)
register(
    "https://github.com/microscopexyz/chainmeta-core/chainmeta/schemas/artifact_schema.json",  # noqa: E501
    common_schema,
)
register(
    "https://github.com/microscopexyz/chainmeta-core/chainmeta/schema/artifact_schema.json",  # noqa: E501
    common_schema,
)


for f in os.listdir(Path(__file__).parent.parent.resolve().joinpath(ContribFolder)):
    filename = os.fsdecode(f)
    if f.endswith(".py"):
        try:
            m = importlib.import_module(f"chainmeta.contrib.{filename[:-3]}")
            if isinstance(m.schema_path, list):
                for p in m.schema_path:
                    register(p, Schema(m.validator, m.translator))
            else:
                register(m.schema_path, Schema(m.validator, m.translator))
        except Exception as e:
            logger.warning(f"Failed to load {filename}: {e}")
