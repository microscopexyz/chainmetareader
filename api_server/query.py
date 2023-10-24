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

from fastapi import APIRouter, Header, Query

from chainmeta_reader import search_chainmeta
from chainmeta_reader import db

router = APIRouter()


@router.get("/v1/query")
@router.get("/search_chainmeta")
@router.get("/api/search")
async def search(
        chain: str = Query(None),
        address: str = Query(None),
        token: Optional[str] = Header(None),
):
    if token is None:
        return "missing required header [TOKEN]"
    if not is_token_valid(token):
        return "header [TOKEN] is not exist or invalid"
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


# @router.get("/add_token")
async def add_token(token: str = Query(None), belongs_to: str = Query(None)):
    db.add_api_token(token, belongs_to)


@router.get("/find_valid_token")
async def add_token(token: str = Query(None)):
    api_token: dict = db.find_valid_token(token)
    return api_token


def is_token_valid(token):
    api_token: dict = db.find_valid_token(token)
    if not api_token:
        return False
    return True
