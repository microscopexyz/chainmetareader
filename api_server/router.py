from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


@router.get("/notes/", response_model=str)
async def read_notes():
    return "ok"


if __name__ == '__main__':
    print("run on")
    import asyncio
    import time


    async def loop():
        while (True):
            t = time.time()
            ret = await read_notes()
            # ret=await get_all_up(600011)
            print(time.time() - t)
            await asyncio.sleep(0.1)


    asyncio.run(loop())
    while (True):
        time.sleep(0.1)
