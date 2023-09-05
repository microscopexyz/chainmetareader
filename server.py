import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

from api_server import search_api

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
