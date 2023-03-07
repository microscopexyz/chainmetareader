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

from jsonschema import validate as js_validate

from chainmeta_reader.constants import ValidatorType


class Validator(object):
    def __init__(self, *, validator_type: ValidatorType = ValidatorType.Global):
        self.validator_type = validator_type
        schema_file = (
            pathlib.Path(__file__).parent.resolve().joinpath("meta_schema.json")
        )

        with open(schema_file) as sf:
            self.schema = json.load(sf)

    def validate(self, metadata: dict):
        js_validate(instance=metadata, schema=self.schema)

    def to_string(self):
        prefix = "chainmeta"
        validator = "validator"
        '"{{%s.%s.%s}}"' % (prefix, validator, self.validator_type)


class ChaintoolValidator(Validator):
    def __init__(self, config_rules):
        super().__init__(validator_type=ValidatorType.ChainTool)
        self.rules = config_rules

    def validate(self, input_address):

        # check the global format
        super().validate(input_address)

        # TODO add the chaintool related format checking logic here


class CoinBaseValidator(Validator):
    def __init__(self, config_rules):
        super().__init__(validator_type=ValidatorType.CoinBase)
        self.rules = config_rules

    def validate(self, input_address):
        # check the global format
        super().validate(input_address)

        # TODO add coinbase related format checking logic


class GoPlusValidator(Validator):
    def __init__(self, config_rules):
        super().__init__(validator_type=ValidatorType.GoPlus)
        self.rules = config_rules

    def validate(self, input_address):
        # check the global format
        super().validate(input_address)

        # TODO add GoPlus related format checking logic
