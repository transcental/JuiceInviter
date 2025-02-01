import os

import aiohttp
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

load_dotenv()


class Environment:
    def __init__(self):
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "unset")
        self.slack_user_token = os.environ.get("SLACK_USER_TOKEN", "unset")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "unset")
        self.slack_cookie = os.environ.get("SLACK_COOKIE", "unset")
        self.slack_browser_token = os.environ.get("SLACK_BROWSER_TOKEN", "unset")


        self.port = int(os.environ.get("PORT", 3000))

        self.airtable_api_key = os.environ.get("AIRTABLE_API_KEY", "unset")
        self.airtable_base_id = os.environ.get("AIRTABLE_BASE_ID", "unset")
        self.airtable_table_id = os.environ.get("AIRTABLE_TABLE_ID", "unset")

        unset = [key for key, value in self.__dict__.items() if value == "unset"]

        if unset:
            raise ValueError(f"Missing environment variables: {', '.join(unset)}")


        self.aiohttp_session: aiohttp.ClientSession = None  # type: ignore - initialised in async_init which happens at program start
        self.slack_client = AsyncWebClient(token=self.slack_bot_token)


    async def async_init(self):
        """Initialises the aiohttp session"""
        self.aiohttp_session = aiohttp.ClientSession()

    async def async_close(self):
        """Closes the aiohttp session"""
        if self.aiohttp_session:
            await self.aiohttp_session.close()


env = Environment()
