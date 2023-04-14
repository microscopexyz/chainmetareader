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

import chainmeta_reader
from chainmeta_reader.contrib.chaintool import ChaintoolTranslator


@pytest.mark.parametrize(
    "input_file",
    [
        "chaintool_sample.json",
    ],
)
def test_chaintool_translator(input_file: str):
    data_folder = pathlib.Path(__file__).parent.resolve().joinpath("data")
    resolved_input_file = data_folder.joinpath(input_file)
    with open(resolved_input_file) as f:
        # Load Chaintool artifact
        metadata = chainmeta_reader.load(f, artifact_base_path=data_folder)
        raw_metadata = metadata["chainmetadata"]["raw_artifact"]
        intermediate_metadata = metadata["chainmetadata"]["artifact"]

        # Translate back to Chaintool metadata schema
        translator = ChaintoolTranslator()
        raw_metadata2 = [
            translator.from_common_schema(item) for item in intermediate_metadata
        ]
        raw_metadata2_dict = {}
        for item in raw_metadata2:
            raw_metadata2_dict[item["address"]] = item

        # compare raw_metadata with raw_metadata2
        assert len(list(raw_metadata)) == len(raw_metadata2_dict)
        for raw_item in raw_metadata:
            address = raw_item["address"]
            for filed_name in dict(raw_item).keys():
                if filed_name == "source":
                    continue
                assert ChaintoolTranslator.normalize_key(
                    raw_item[filed_name]
                ) == ChaintoolTranslator.normalize_key(
                    raw_metadata2_dict.get(address)[filed_name]
                )
