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

from chainmeta_reader.validator import ValidatorError

file_prefix = "file:///"


def local_loader(uri: str, *, base_path: pathlib.Path = None) -> str:
    if not base_path:
        raise ValidatorError("missing artifact base path for local artifact file")
    relative_path = uri[len(file_prefix) :]
    resolved_path = base_path.joinpath(relative_path)
    with open(resolved_path) as f:
        return f.read()


def s3_loader(uri: str, **kw) -> str:
    pass


def http_loader(uri: str, **kw) -> str:
    pass


def json_parser(c: str) -> object:
    return json.loads(c)


def csv_parser(c: str) -> object:
    pass


parsers = {
    "json": json_parser,
    "JSON": json_parser,
    "csv": csv_parser,
    "CSV": csv_parser,
}


def load(uri: str, fileformat: str, *, base_path: pathlib.Path = None) -> object:
    loader = local_loader if uri.lower().startswith(file_prefix) else None
    parser = parsers.get(fileformat)
    if loader and parser:
        return parser(loader(uri, base_path=base_path))
