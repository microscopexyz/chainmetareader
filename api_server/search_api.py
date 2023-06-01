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

from fastapi import APIRouter, Query

from chainmeta_reader import search_chainmeta

router = APIRouter()


@router.get("/search_chainmeta")
async def search(chain: str = Query(None), address: str = Query(None)):
    if address is None:
        return "missing parameter address"
    if chain is None:
        results = search_chainmeta(filter={"address": address})
    else:
        results = search_chainmeta(
            filter={
                "address": address,
                "chain": chain,
            }
        )
    return results
