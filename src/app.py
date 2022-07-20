from typing import Callable

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
from confluence import *
from slack_sdk import WebClient

APP_TOKEN = "xapp-1-A03NNN2H4E5-3751520877734-f768a856842e41c888bee8001d97493ebaabf6999f3c82bc8e88761cb73012db"
BOT_TOKEN = "xoxb-3751443857062-3781888064192-fFS8sRPyJOOQNGMR0uZR06W4"
app = App(token=BOT_TOKEN)

message = ""
subpage_name = ""
channel = ""
user = ""


@app.event("app_mention")
def handle_app_mention_events(body: dict, say: Callable):
    print(body)
    global message, subpage_name, channel, user
    blocks = _create_block_for_categories()
    say(
        blocks=blocks,
        text="Pick a category to save this message"
    )
    bot_id = body.get("event", {}).get("text").split()[0]
    message = body.get("event", {}).get("text").replace(bot_id, "").strip()
    channel = body.get("event", {}).get("channel")
    user = body.get("event", {}).get("user")
    event_time = body["event_time"]
    subpage_name = datetime.fromtimestamp(event_time).strftime('%B-%Y')


@app.action("static_select-action")
def handle_some_action(ack, body, logger):
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
