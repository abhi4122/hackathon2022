from typing import Callable

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
from confluence import *


APP_TOKEN = "xapp-1-A03NNN2H4E5-3751520877734-f768a856842e41c888bee8001d97493ebaabf6999f3c82bc8e88761cb73012db"
BOT_TOKEN = "xoxb-3751443857062-3781888064192-fFS8sRPyJOOQNGMR0uZR06W4"
app = App(token=BOT_TOKEN)


@app.event("app_mention")
def handle_app_mention_events(body: dict, say: Callable):
    print(body)
    say("got it")
    bot_id = body.get("event", {}).get("text").split()[0]
    message = body.get("event", {}).get("text").replace(bot_id, "").strip()
    print(message)
    event_time = body["event_time"]
    subpage_name = datetime.fromtimestamp(event_time).strftime('%B-%Y')
    print(subpage_name)
    page_id = get_page_id(subpage_name)
    if page_id is None:
        page_id = create_page(subpage_name)
    # update_page(page_id, message)


if __name__ == "__main__":
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()