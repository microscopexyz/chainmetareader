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

from chainmeta_reader.artifact import load as _load
from chainmeta_reader.schema import resolve as _resolve
from chainmeta_reader.validator import JsonValidator, Validator, ValidatorError

global_validator = Validator()


def validate(
    fp,
    *,
    ignore_unrecognized=True,
    additional_schemas={},
    artifact_base_path=None,
    **kw
):
    """Validate ``fp`` (a ``.read()``-supporting file-like object containing
    an open chain metadata document) against the open chain metadata rule set.
    """
    validates(
        fp.read(),
        ignore_unrecognized=ignore_unrecognized,
        additional_schemas=additional_schemas,
        artifact_base_path=artifact_base_path,
    )


def validates(
    s: str,
    *,
    ignore_unrecognized=True,
    additional_schemas={},
    artifact_base_path=None,
    **kw
):
    """Validate ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing
    an open chain metadata document) against the open chain metadata rule set.
    """
    metadata = json.loads(s)

    # Global validation
    global_validator.validate(metadata)
    raw_schema = metadata["chainmetadata"]["schema"]
    artifacts = metadata["chainmetadata"]["artifact"]

    # Artifact validation
    schema = _resolve(raw_schema) or additional_schemas.get(raw_schema)
    if not schema and not ignore_unrecognized:
        raise ValidatorError("unrecognized artifact schema")
    if not schema:
        return metadata
    artifact_validator = JsonValidator(schema=schema)
    loaded_artifacts = []
    for artifact in artifacts:
        loaded_artifact = _load(
            artifact["path"],
            fileformat=artifact["fileformat"],
            base_path=artifact_base_path,
        )
        artifact_validator.validate(loaded_artifact)
        loaded_artifacts += loaded_artifact["metadata"]
    if loaded_artifact:
        metadata["chainmetadata"]["loaded_artifact"] = loaded_artifacts

    return metadata


def load(
    fp, ignore_unrecognized=True, additional_schemas={}, artifact_base_path=None, **kw
):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    an open chain metadata document) to a Python object.
    """
    return loads(
        fp.read(),
        ignore_unrecognized=ignore_unrecognized,
        additional_schemas=additional_schemas,
        artifact_base_path=artifact_base_path,
        **kw,
    )


def loads(
    s: str,
    *,
    ignore_unrecognized=True,
    additional_schemas={},
    artifact_base_path=None,
    **kw
):
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing
    an open chain metadata document) to a Python object.
    """
    return validates(
        s,
        ignore_unrecognized=ignore_unrecognized,
        additional_schemas=additional_schemas,
        artifact_base_path=artifact_base_path,
        **kw,
    )


__all__ = ["validate", "validates", "load", "loads", "global_validator"]
