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
from typing import Optional


def resolve(schema: str) -> Optional[pathlib.Path]:
    prefix = "https://github.com/openchainmeta/chainmetareader/chainmeta_reader/"
    if not schema or not schema.lower().startswith(prefix):
        return None

    relative_path = schema[len(prefix) :]
    return pathlib.Path(__file__).parent.resolve().joinpath(relative_path)
