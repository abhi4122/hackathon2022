from typing import Callable

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
from confluence import *


APP_TOKEN = "xapp-1-A03NNN2H4E5-3751520877734-f768a856842e41c888bee8001d97493ebaabf6999f3c82bc8e88761cb73012db"
BOT_TOKEN = "xoxb-3751443857062-3781888064192-fFS8sRPyJOOQNGMR0uZR06W4"
app = App(token=BOT_TOKEN)


@app.event("app_mention")
def mention_handler(body: dict, say: Callable):
    print(body)
    say("got it")
    msg = body["event"]["text"]
    print(msg)
    event_time = body["event_time"]
    ts = datetime.fromtimestamp(event_time).strftime('%B-%Y')
    print(ts)
    page_id = get_page_id(ts)
    if page_id is None:
        new_page_id = create_page(ts)


if __name__ == "__main__":
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()