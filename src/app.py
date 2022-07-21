#
# Copyright (c) 2022 by Delphix-Hackathon. All rights reserved.
#

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
import re
from confluence import *
from slack_sdk import WebClient
import logging

# delphix-digest-tokens
APP_TOKEN = "xapp-1-A03QAMVE15K-3815922906135-9d94c5cf8500a902aeda0cda43048674d212474302a1790d9ed46242dd2a2b24"
BOT_TOKEN = "xoxb-3751443857062-3853451302448-eeHQ50snUL7IyqSi9eX3iGNm"

app = App(token=BOT_TOKEN)

message = ""
subpage_name = ""
channel = ""
user = ""


@app.event("app_mention")
@app.event("message")
def handle_app_mention_events(body: dict):
    """
    Method to capture app_mention and instant message
    events triggered from slack bot, capture message body
    and trigger Ephemeral block kit to confirm category

    :param body : Body of the message posted on slack
    :type body: ```dict```
    """
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
def handle_some_action(ack, body):
    """
    Method to handle select action for Block kit,
    capture category and create/update confluence page
    based on received data

    :param ack : receive acknowledgement from slack
    :type  ack : ```ack```
    :param body : Body of the select kit builder response
        posted on slack
    :type body: ```dict```
    """
    ack()
    logging.info(body)
    try:
        category = body["actions"][0]["selected_option"]["text"]["text"]
        logging.info(f"Message will be posted to following category: {category}")
        logging.info(f"Message to be posted: {message}")
        logging.info(f"Name of the page the message will be appended to: {subpage_name}")
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
    """
    Method to format message captured by slack bot

    :param client : WebClient Object
    :type  client : ```object```
    :param msg : message to be formatted
    :type msg: ```str```
    :param msg_time : msg post time retrieved from slack
    :type  msg_time : ```str```
    :param channel_name : name of the channel where msg was
        posted retrieved from slack
    :type  channel_name : ```str```
    """
    all_words = msg.split()
    new_msg = ""
    for word in all_words:
        if re.search("<@.*>", word):
            user_id = word.replace("<@", "").replace(">", "")
            user_detail = client.users_info(user=user_id)
            new_msg = new_msg + " " + "<b>" + user_detail.get('user').get('real_name') + "</b>"
        elif ':' in word:
            pass
        else:
            new_msg = new_msg + " " + word
    return new_msg.strip() + f" <em><span style=\"color:#97a0af\">(Posted on {msg_time} at #{channel_name})</span></em>"


def _create_block_for_categories():
    """
    Method to create content for BLock Kit
    """
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello, *Delphix Digest* wants to know where you'd like to save this message.\n\n *Please "
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
