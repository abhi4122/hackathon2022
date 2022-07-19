from typing import Callable

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
from confluence import *
from slack_sdk import WebClient


APP_TOKEN = "xapp-1-A03NNN2H4E5-3751520877734-f768a856842e41c888bee8001d97493ebaabf6999f3c82bc8e88761cb73012db"
BOT_TOKEN = "xoxb-3751443857062-3781888064192-fFS8sRPyJOOQNGMR0uZR06W4"
app = App(token=BOT_TOKEN)


@app.event("app_mention")
def handle_app_mention_events(body: dict, say: Callable):
    try:
        bot_id = body.get("event", {}).get("text").split()[0]
        message = body.get("event", {}).get("text").replace(bot_id, "").strip()
        channel = body.get("event", {}).get("channel")
        user = body.get("event", {}).get("user")

        event_time = body["event_time"]
        subpage_name = datetime.fromtimestamp(event_time).strftime('%B-%Y')
        page_id = get_page_id(subpage_name)

        if page_id is None:
            page_id = create_page(subpage_name)
        update_page(page_id, message, 'Recognitions')
    except BaseException as exp:
        raise exp
    else:
        client = WebClient(token=BOT_TOKEN)
        client.chat_postEphemeral(
            channel=channel,
            text="Your update has been successfully appended to Newsletter",
            user=user,
        )


if __name__ == "__main__":
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()
