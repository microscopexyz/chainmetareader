#!/usr/bin/env python3

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

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

from api_server import kya_search, search_api

app = FastAPI()
cookie_key = "chaintool_build_great_job"


@app.middleware("http")
async def log_request(request, call_next):
    print(f"{request.method} {request.url} {request.query_params} {request.session}")
    response = await call_next(request)
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    # do something with body ...
    ret = Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
    try:
        body = json.loads(body, strict=False)
    except Exception:
        pass
    print(body)
    return ret


app.add_middleware(SessionMiddleware, secret_key=cookie_key)
app.include_router(search_api.router, prefix="/api")
app.include_router(kya_search.router, prefix="/kya")


@app.get("/", response_class=PlainTextResponse)
async def app_check():
    return "ok"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="warning")
