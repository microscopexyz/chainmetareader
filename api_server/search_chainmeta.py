from fastapi import APIRouter, Request, Query

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


@router.get("/search_chainmeta")
async def search(chain: str = Query(None), address: str = Query(None)):
    if address is None:
        return 'missing parameter address'
    if chain is None:
        results = search_chainmeta(
            filter={
                "address": address
            }
        )
    else:
        results = search_chainmeta(
            filter={
                "address": address,
                "chain": chain,
            })
    return results
