from typing import Callable

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
import re
from confluence import *
from slack_sdk import WebClient

# professor
APP_TOKEN = "xapp-1-A03NNN2H4E5-3831783264532-2630d3d2503861c0474d18729c09df8ec4cf28ae20025d36d2899e4d8e56e1eb"
BOT_TOKEN = "xoxb-3751443857062-3781888064192-bL05ZXVbCNB9RUHLtGmPjvvA"

# newsletter
#APP_TOKEN = "xapp-1-A03QL9C2ND7-3822744932038-f7ee5f17a7eeeb16be851937bc4746762307512d857cdfad123b0ec220e161cc"
#BOT_TOKEN = "xoxb-3751443857062-3823639890851-4vjHicpxdKeKFjgQ7KYXCohe"
app = App(token=BOT_TOKEN)

message = ""
subpage_name = ""
channel = ""
user = ""


@app.event("app_mention")
def handle_app_mention_events(body: dict):
    print("app_mention called")
    print(body)
    global message, subpage_name, channel, user
    blocks = _create_block_for_categories()
    bot_id = "<@" + body.get("authorizations")[0].get("user_id") + ">"
    message = body.get("event", {}).get("text").replace(bot_id, "").strip()
    channel = body.get("event", {}).get("channel")
    user = body.get("event", {}).get("user")
    event_time = body["event_time"]
    subpage_name = datetime.fromtimestamp(event_time).strftime('%B-%Y')
    msg_time = datetime.fromtimestamp(event_time).strftime('%d %B %H:%M:%S')
    client = WebClient(token=BOT_TOKEN)
    channel_details = client.conversations_info(channel=channel)
    message = _format_message(client, message, msg_time, channel_details.get('channel').get('name'))
    client.chat_postEphemeral(
        channel=channel,
        blocks=blocks,
        text="Pick a category to save this message",
        user=user,
    )


@app.action("static_select-action")
def handle_some_action(ack, body, logger):
    print("static_select-action called")
    ack()
    logger.info(body)
    try:
        category = body["actions"][0]["selected_option"]["text"]["text"]
        print(category)
        print(message)
        print(subpage_name)
        page_id = get_page_id(subpage_name)
        if page_id is None:
            page_id = create_page(subpage_name)
        update_page(page_id, message, category)
    except BaseException as e:
        raise e
    else:
        client = WebClient(token=BOT_TOKEN)
        client.chat_postEphemeral(
            channel=channel,
            text=f"Your message has been successfully appended to {subpage_name} newsletter under {category}",
            user=user,
        )


def _format_message(client, msg, msg_time, channel_name):
    all_words = msg.split()
    new_msg = ""
    for word in all_words:
        if re.search("<@.*>", word):
            user_id = word.replace("<@", "").replace(">", "")
            user_detail = client.users_info(user=user_id)
            new_msg = new_msg + " " + "<b>" + user_detail.get('user').get('real_name') + "</b>"
        else:
            new_msg = new_msg + " " + word
    return new_msg.strip() + f" <em><span style=\"color:#97a0af\">(Posted on {msg_time} at #{channel_name})</span></em>"


def _create_block_for_categories():
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello, *Professor* wants to know where you'd like to save this message.\n\n *Please "
                        "select a category:* "
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a category from the dropdown list"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a category",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Recognitions",
                            "emoji": True
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Work Anniversaries",
                            "emoji": True
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Release Updates",
                            "emoji": True
                        },
                        "value": "value-2"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Project Updates",
                            "emoji": True
                        },
                        "value": "value-3"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Initiatives",
                            "emoji": True
                        },
                        "value": "value-4"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Ted Talks - Python",
                            "emoji": True
                        },
                        "value": "value-5"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Fun Activities and Events",
                            "emoji": True
                        },
                        "value": "value-6"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "New Joiners",
                            "emoji": True
                        },
                        "value": "value-7"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Miscellaneous",
                            "emoji": True
                        },
                        "value": "value-8"
                    }
                ],
                "action_id": "static_select-action"
            }
        }
    ]


if __name__ == "__main__":
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()
