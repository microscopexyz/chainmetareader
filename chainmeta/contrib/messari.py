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

from typing import Optional

from chainmeta.metadata import ChainmetaItem, ITranslator
from chainmeta.validator import IValidator


class MessariTranslator(ITranslator):
    def to_common_schema(self, raw_metadata) -> Optional[ChainmetaItem]:
        # Add your implementation here
        pass

    def from_common_schema(
        self, common_schema_metadata: ChainmetaItem
    ) -> Optional[object]:
        # Add your implementation here
        pass


class MessariValidator(IValidator):
    def validate(self, metadata: object):
        # Add your implementation here
        return


schema_path = "_schema.json"

validator = MessariValidator()
translator = MessariTranslator()
