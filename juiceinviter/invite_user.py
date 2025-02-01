from juiceinviter.env import env
import json

async def invite_user_to_slack(email):
    headers = {
        "Cookie": f"d={env.slack_cookie}",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {env.slack_browser_token}"
    }
    
    data = {
        "invites": [
            {
                "email": email,
                "type": "restricted",
                "mode": "manual"
            }
        ],
        "restricted": True,
        "channels": "C039PAG1AV7,C088UF12N1Z"
    }

    async with env.aiohttp_session.post("https://slack.com/api/users.admin.inviteBulk", headers=headers, data=json.dumps(data)) as response:
        response_json = await response.json()
        # Debugging: Log response
        if not response_json["ok"]:
            return False
        return True