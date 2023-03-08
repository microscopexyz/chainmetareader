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
import pathlib

import pytest
from jsonschema import ValidationError

import chainmeta_reader
from chainmeta_reader.validator import (
    ChaintoolValidator,
    GoPlusValidator,
    IValidator,
    Validator,
)


@pytest.mark.parametrize(
    "input_file,is_valid",
    [
        ("empty.json", False),
        ("missing_community.json", False),
        ("chaintool_meta.json", True),
        ("coinbase_sample.json", True),
        ("coinbase_invalid_sample.json", False),
    ],
)
def test_validate(input_file: str, is_valid: bool):
    data_folder = pathlib.Path(__file__).parent.resolve().joinpath("data")
    resolved_input_file = data_folder.joinpath(input_file)
    with open(resolved_input_file) as fp:
        try:
            chainmeta_reader.validate(fp, artifact_base_path=data_folder)
        except ValidationError as e:
            print(e)
            assert is_valid is False
        else:
            assert is_valid


@pytest.mark.parametrize(
    "validator, s",
    [
        (Validator(), "chainmeta.validator.global"),
        (ChaintoolValidator(None), "chainmeta.validator.ct"),
        (GoPlusValidator(None), "chainmeta.validator.gp"),
    ],
)
def test_to_string(validator: IValidator, s: str):
    assert validator.to_string() == s
