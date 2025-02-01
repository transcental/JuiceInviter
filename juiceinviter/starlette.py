from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from juiceinviter.__main__ import app as slack_app, main

req_handler = AsyncSlackRequestHandler(slack_app)


async def endpoint(req: Request):
    return await req_handler.handle(req)


app = Starlette(
    debug=True,
    routes=[
        Route(path="/slack/events", endpoint=endpoint, methods=["POST"]),
    ],
    lifespan=main,
)
