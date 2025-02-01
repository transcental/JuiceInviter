import asyncio
import contextlib
from slack_bolt.async_app import AsyncApp
from dotenv import load_dotenv
import os
from starlette.applications import Starlette
import uvloop
import uvicorn

from juiceinviter.check_users import check_users
from juiceinviter.env import env

load_dotenv()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


app = AsyncApp(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
)

@contextlib.asynccontextmanager
async def main(_app: Starlette):
    await env.async_init()
    asyncio.create_task(check_users())
    try:
        yield
    finally:
        await env.async_close()

def start():
    uvicorn.run(
        "juiceinviter.starlette:app",
        host="0.0.0.0",
        port=env.port,
        log_level="info"
    )

if __name__ == "__main__":
    start()
