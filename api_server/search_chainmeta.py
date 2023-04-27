from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List

from chainmeta_reader import search_chainmeta

router = APIRouter()


@router.get("/search_chainmeta/{chain}/{address}")
async def search(chain: str, address: str, request: Request):
    if address is None or chain is None:
        return 'missing parameter address or chain'
    results = search_chainmeta(
        filter={
            "address": address,
            "chain": chain,
        }
    )

    return results
