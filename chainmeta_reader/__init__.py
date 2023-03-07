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
from typing import List

from chainmeta_reader.validator import Validator

# TODO: add other validators to the list
validators: List[Validator] = [Validator()]


def validate(fp):
    """Validate ``fp`` (a ``.read()``-supporting file-like object containing
    an open chain metadata document) against the open chain metadata rule set.
    """
    validates(fp.read())


def validates(s: str):
    """Validate ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing
    an open chain metadata document) against the open chain metadata rule set.
    """
    metadata = json.loads(s)
    for v in validators:
        v.validate(metadata)
    return metadata


def load(fp, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    an open chain metadata document) to a Python object.
    """
    return loads(fp.read(), **kw)


def loads(s: str, **kw):
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing
    an open chain metadata document) to a Python object.
    """
    return validates(s)
