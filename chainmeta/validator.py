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
from abc import ABC
from pathlib import Path
from typing import Optional

from jsonschema import Draft7Validator, TypeChecker, validators

from chainmeta.config import default_config
from chainmeta.constants import ArtifactSchemaFile, Field, MetaSchemaFile, SchemaFolder


def value_checker(valid_values):
    return lambda checker, instance: (
        checker.is_type(instance, "string") and instance in valid_values
    )


class IValidator(ABC):
    def validate(self, metadata: object):
        pass


class JsonValidator(IValidator):
    def __init__(self, *, schema: Path, type_checker: Optional[TypeChecker] = None):
        with open(schema) as sf:
            if type_checker is None:
                self.validator = Draft7Validator(schema=json.load(sf))
            else:
                custom_validator = validators.extend(
                    Draft7Validator, type_checker=type_checker
                )
                self.validator = custom_validator(schema=json.load(sf))

    def validate(self, metadata: object):
        self.validator.validate(metadata)


common_metadata_validator = JsonValidator(
    schema=Path(__file__).parent.resolve().joinpath(SchemaFolder, MetaSchemaFile)
)

type_checker = Draft7Validator.TYPE_CHECKER.redefine_many(
    {
        Field.CATEGORY.value: value_checker(default_config.Categories),
        Field.ENTITY.value: value_checker(default_config.Entities),
        Field.SOURCE.value: value_checker(default_config.Sources),
        Field.CHAIN.value: value_checker(default_config.Chains),
    }
)
common_artifact_validator = JsonValidator(
    schema=Path(__file__).parent.resolve().joinpath(SchemaFolder, ArtifactSchemaFile),
    type_checker=type_checker,
)
