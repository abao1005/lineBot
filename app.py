import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent
from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["initial", "start", "depart_or_arrive", "time",
            "station", "get_station", "show", "kouho", "tmp", "tmp2", "bonus"],
    transitions=[
        {
            "trigger": "go_start",
            "source": "initial",
            "dest": "start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "depart_or_arrive",
            "conditions": "is_going_to_depart_or_arrive",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "bonus",
            "conditions": "is_going_to_bonus",
        },
        {
            "trigger": "advance",
            "source": "depart_or_arrive",
            "dest": "time",
            "conditions": "is_going_to_time",
        },
        {
            "trigger": "advance",
            "source": "time",
            "dest": "station",
            "conditions": "is_going_to_station",
        },
        {
            "trigger": "advance",
            "source": "station",
            "dest": "get_station",
            "conditions": "is_going_to_get_station",
        },
        {
            "trigger": "advance",
            "source": "get_station",
            "dest": "show",
            "conditions": "is_going_to_show",
        },
        {
            "trigger": "advance",
            "source": "get_station",
            "dest": "kouho",
            "conditions": "is_going_to_kouho",
        },
        {
            "trigger": "advance",
            "source": "tmp2",
            "dest": "show",
            "conditions": "is_going_to_show",
        },
        {
            "trigger": "advance",
            "source": "kouho",
            "dest": "tmp",
            "conditions": "is_going_to_tmp",
        },
        {
            "trigger": "advance",
            "source": "tmp",
            "dest": "tmp2",
            "conditions": "is_going_to_tmp2",
        },
        {
            "trigger": "go_back",
            "source": ["show", "tmp2"],
            "dest": "start",
            "conditions": "is_go_back"
        },
        {
            "trigger": "restart",
            "source": ["bonus", "depart_or_arrive", "station", "time", "get_station", "kouho", "show", "start", "tmp", "tmp2"],
            "dest": "start",
            "conditions": "is_restart"
        }
    ],
    initial="initial",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if machine.state == "initial":
            machine.go_start(event)
            break
        if isinstance(event, PostbackEvent):
            #dateTime = event.postback.params["datetime"]
            machine.advance(event)
            # print(f"{dateTime}")
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                if isinstance(event.message.text, str):
                    if event.message.text == "重新查詢":
                        machine.restart(event)
                    elif event.message.text == "謝謝!":
                        machine.go_back(event)
                    else:
                        machine.advance(event)

        #print(f"\nFSM STATE: {machine.state}")
        #print(f"REQUEST BODY: \n{body}")
        # if response == False:
        #    send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show_fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
