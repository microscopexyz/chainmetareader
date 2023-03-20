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

from chainmeta_reader import (
    ChaintoolTranslator,
    denormalize,
    load,
    normalize,
)


@pytest.mark.parametrize(
    "input_file",
    [
        ("chaintool_sample.json"),
    ],
)
def test_chaintool_translator(input_file: str):
    data_folder = pathlib.Path(__file__).parent.resolve().joinpath("data")
    resolved_input_file = data_folder.joinpath(input_file)
    with open(resolved_input_file) as f:
        # Load Chaintool artifact
        metadata = load(f, artifact_base_path=data_folder)
        raw_metadata = metadata["chainmetadata"]["loaded_artifact"]

        # Translate to intermediate metadata schema
        intermediate_metadata = normalize(
            metadata["chainmetadata"]["loaded_artifact"], ChaintoolTranslator
        )

        # Translate back to Coinbase metadata schema
        raw_metadata2 = denormalize(intermediate_metadata, ChaintoolTranslator)
        raw_metadata2_dict = {}
        for item in raw_metadata2:
            raw_metadata2_dict[item["address"]] = item

        # compare raw_metadata with raw_metadata2
        assert len(list(raw_metadata)) == len(raw_metadata2_dict)
        for raw_item in raw_metadata:
            address = raw_item["address"]
            for filed_name in dict(raw_item).keys():
                assert raw_item[filed_name] == raw_metadata2_dict.get(address)[filed_name]
