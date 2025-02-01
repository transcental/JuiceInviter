import logging
from slack_sdk.errors import SlackApiError
from juiceinviter.env import env
from pyairtable import Api
from asyncio import sleep

from juiceinviter.invite_user import invite_user_to_slack

airtable_client = Api(
    api_key = env.airtable_api_key
)

invite_table = airtable_client.table(env.airtable_base_id, env.airtable_table_id)
CHANNEL_ID = "C088UF12N1Z"

async def check_users():
    await env.slack_client.chat_postMessage(
        channel="U054VC2KM9P",
        text = "Juicing started"
    )
    users = invite_table.all(formula="NOT({inChannel})")
    errors = []
    for invite in users:
        # check if the user is already in the channel
        try:
            try:
                user = await env.slack_client.users_lookupByEmail(email=invite["fields"]["email"])
            except SlackApiError as e:
                if e.response["error"] == "ratelimited":
                    retry_after = int(e.response.headers.get("Retry-After", 1))
                    logging.info(f"Rate limited, retrying in {retry_after} seconds.")
                    await sleep(retry_after)
                    user = await env.slack_client.users_lookupByEmail(email=invite["fields"]["email"])
                elif e.response["error"] == "users_not_found":
                    res = await invite_user_to_slack(invite["fields"]["email"])
                    if not res:
                        errors.append(invite["fields"]["email"])
                    else:
                        invite_table.update(invite["id"], {"inChannel": True})
                    continue
                else:
                    logging.error(f"Something really failed: {e}", exc_info=True)
                    continue
            user_id = user.get("user", {}).get("id", "")
            await env.slack_client.conversations_invite(
                channel = CHANNEL_ID,
                users=[user_id],
                token=env.slack_user_token
            )
            logging.info(f"Invited {invite['fields']['email']} to the channel")
            try:
                await env.slack_client.chat_postMessage(
                    channel=user_id,
                    text = f"hello! you registered interest in :juice: <#{CHANNEL_ID}> so you've been added to the channel. you can ask questions and show off what you're working on here! welcome!"
                )
                invite_table.update(invite["id"], {"inChannel": True})
            except SlackApiError as e:
                if e.response["error"] == "ratelimited":
                    retry_after = int(e.response.headers.get("Retry-After", 1))
                    logging.info(f"Rate limited, retrying in {retry_after} seconds.")
                    await sleep(retry_after)
                    await env.slack_client.chat_postMessage(
                        channel=user_id,
                        text = f"hello! you registered interest in :juice: <#{CHANNEL_ID}> so you've been added to the channel. you can ask questions and show off what you're working on here! welcome!"
                    )
            logging.info(f"Messaged {invite['fields']['email']}")
        except SlackApiError as e:
            if e.response.get("errors", [{}])[0].get('error', '') == "already_in_channel":
                logging.info(f"{invite['fields']['email']} is already in the channel")
                # update record
                invite_table.update(invite["id"], {"inChannel": True})
            elif e.response["error"] == "ratelimited":
                retry_after = int(e.response.headers.get("Retry-After", 1))
                logging.info(f"Rate limited, retrying in {retry_after} seconds.")
                await sleep(retry_after)
                user = await env.slack_client.users_lookupByEmail(email=invite["fields"]["email"])
                user_id = user.get("user", {}).get("id", "")
                await env.slack_client.conversations_invite(
                    channel = CHANNEL_ID,
                    users=[user_id]
                )
                await env.slack_client.chat_postMessage(
                    channel=user_id,
                    text = f"hello! you registered interest in :juice: <#{CHANNEL_ID}> so you've been added to the channel. you can ask questions and show off what you're working on here! welcome!"
                )
                invite_table.update(invite["id"], {"inChannel": True})
                
    print('Juicing complete!')
    await env.slack_client.files_upload_v2(
            channel="U054VC2KM9P",
            content=str(errors),
            initial_comment=f"Juicing complete! {len(errors)} errors.",
        )
        
    await sleep(5*60)
