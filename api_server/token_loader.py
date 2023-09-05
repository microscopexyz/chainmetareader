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
import os


def is_token_valid(token: str):
    current_path = os.path.dirname(__file__)
    print(current_path)
    with open(r"api_tokens.json", "r") as tokens:
        token_arr = json.load(tokens)
        for t in token_arr:
            if t["token"] == token:
                return True
        return False
