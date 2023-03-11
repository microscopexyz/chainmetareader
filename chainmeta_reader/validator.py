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
from abc import ABC, abstractmethod

from jsonschema import validate as js_validate

from chainmeta_reader.constants import ValidatorType


class IValidator(ABC):
    @abstractmethod
    def validate(self, metadata: dict):
        pass

    def __init__(self, *, validator_type: ValidatorType):
        self.validator_type = validator_type

    def to_string(self) -> str:
        prefix = "chainmeta"
        validator = "validator"
        return f"{prefix}.{validator}.{self.validator_type}"


class JsonValidator(object):
    def __init__(self, *, schema: dict):
        with open(schema) as sf:
            self.schema = json.load(sf)

    def validate(self, metadata: dict):
        js_validate(instance=metadata, schema=self.schema)


class ValidatorError(ValueError):
    def __init__(self, msg):
        ValueError.__init__(self, msg)
        self.msg = msg


class Validator(IValidator):
    def __init__(self):
        self.validator_type = ValidatorType.Global
        schema_file = (
            pathlib.Path(__file__)
            .parent.resolve()
            .joinpath("schemas", "meta_schema.json")
        )
        self._validators = [JsonValidator(schema=schema_file)]

    def validate(self, metadata: dict):
        for v in self._validators:
            v.validate(metadata)


class ChaintoolValidator(IValidator):
    def __init__(self, config_rules):
        super().__init__(validator_type=ValidatorType.ChainTool)
        self.rules = config_rules

    def validate(self, input_address):
        # check the global format
        super().validate(input_address)

        # Example JSON object to validate
        json_obj_path = (
            pathlib.Path(__file__)
            .parent.resolve()
            .joinpath("data", "chainmeta_jsonexample.json")
        )
        with open(json_obj_path, "r") as f2:
            json_obj = json.load(f2)

        try:
            schema_path = (
                pathlib.Path(__file__)
                .parent.resolve()
                .joinpath("data", "chaintool_meta.json")
            )
            # Load the JSON schema from an external file
            with open(schema_path, "r") as f:
                schema = json.load(f)
            js_validate(json_obj, schema)
            print("Validation successful!")
        except ValidatorError as e:
            print("Validation error:", e)


class GoPlusValidator(IValidator):
    def __init__(self, config_rules):
        super().__init__(validator_type=ValidatorType.GoPlus)
        self.rules = config_rules

    def validate(self, input_address):
        # check the global format
        super().validate(input_address)

        # TODO add GoPlus related format checking logic
