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
import pathlib

from jsonschema import Draft7Validator, validators

from chainmeta_reader.config import Config, default_config
from chainmeta_reader.constants import (
    ArtifactSchemaFile,
    Field,
    MetaSchemaFile,
    SchemasFolder,
)


def value_checker(valid_values):
    return lambda checker, instance: (
        checker.is_type(instance, "string") and instance in valid_values
    )


class JsonValidator(object):
    def __init__(self, *, config: Config = default_config, schema: dict):
        type_checker = Draft7Validator.TYPE_CHECKER.redefine_many(
            {
                Field.CATEGORY.value: value_checker(config.Categories),
                Field.ENTITY.value: value_checker(config.Entities),
                Field.SOURCE.value: value_checker(config.Sources),
                Field.CHAIN.value: value_checker(config.Chains),
            }
        )

        with open(schema) as sf:
            custom_validator = validators.extend(
                Draft7Validator, type_checker=type_checker
            )
            self.validator = custom_validator(schema=json.load(sf))

    def validate(self, metadata: dict):
        self.validator.validate(metadata)


class ValidatorError(ValueError):
    def __init__(self, msg):
        ValueError.__init__(self, msg)
        self.msg = msg


class Validator:
    def __init__(self):
        schema_file = (
            pathlib.Path(__file__)
            .parent.resolve()
            .joinpath(SchemasFolder, MetaSchemaFile)
        )
        self._validators = [JsonValidator(config=default_config, schema=schema_file)]

    def validate(self, metadata: dict):
        for v in self._validators:
            v.validate(metadata)


common_artifact_validator = JsonValidator(
    schema=pathlib.Path(__file__)
    .parent.resolve()
    .joinpath(SchemasFolder, ArtifactSchemaFile)
)
