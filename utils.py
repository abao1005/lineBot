import os
import json
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import *
from datetime import datetime

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)

handler = WebhookHandler('f2fb6e2344574326730b094b624ff53a')


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_template_message(reply_token, Dep_or_Arr):
    line_bot_api = LineBotApi(channel_access_token)
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_now_format = "T".join(time_now[:-3].split(" "))
    message = TemplateSendMessage(
        alt_text='請輸入欲查詢之'+Dep_or_Arr+'時間',
        template=ButtonsTemplate(
            thumbnail_image_url="https://www.jorudan.co.jp/com/img/bnr/ogp_jorudan.png",
            title="請輸入欲查詢之"+Dep_or_Arr+"時間",
            text="滾動時間條以選擇 \n(或輸入<重新查詢>以重置選項)",
            actions=[
                DatetimePickerTemplateAction(
                    label="請選擇日期與時間",
                    data="input_time",
                    mode='datetime',
                    initial=time_now_format,
                    max='2080-03-10T23:50',
                    min='1930-01-01T23:50'
                )
                # MessageTemplateAction(
                #    label="感謝",
                #    text="謝謝你!"
                # )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"


def send_ask_DorA_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='請問要查詢出發還是抵達時間?',
        template=ButtonsTemplate(
            thumbnail_image_url="https://www.jorudan.co.jp/com/img/bnr/ogp_jorudan.png",
            title="請問要查詢出發還是抵達時間?",
            text="出發or抵達",
            actions=[
                MessageTemplateAction(
                    label="出發",
                    text="出發"
                ),
                MessageTemplateAction(
                    label="抵達",
                    text="抵達"
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, message)


def send_welcome_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='歡迎使用ジョルダン之轉乘查詢服務!',
        template=ButtonsTemplate(
            thumbnail_image_url="https://www.jorudan.co.jp/com/img/bnr/ogp_jorudan.png",
            title="歡迎使用ジョルダン之轉乘查詢服務!",
            text="請選擇您欲使用之服務",
            actions=[
                MessageTemplateAction(
                    label="轉乘資訊",
                    text="我要搭車啦!幫我查查"
                ),
                URITemplateAction(
                    label="我要直接看網頁!",
                    uri="https://www.jorudan.co.jp/"
                )

                # MessageTemplateAction(
                #    label="抵達",
                #    text="抵達"
                # )

            ]
        )
    )
    line_bot_api.reply_message(reply_token, message)


def send_norigae_message(reply_token, style, start_station, end_station):
    line_bot_api = LineBotApi(channel_access_token)
    bubble_dict = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "起站",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": start_station,
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": []
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "迄站",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": end_station,
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#0367D3",
            "spacing": "md",
            "height": "154px",
            "paddingTop": "22px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": style
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "謝謝!",
                        "text": "謝謝!"
                    }
                }
            ]
        }
    }
    d1 = json.dumps(bubble_dict)
    d2 = json.loads(d1)
    message = FlexSendMessage(
        alt_text="乗換案内",
        contents=d2
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def send_kouho_message(reply_token, eki_S, eki_E, kouho_block_S, kouho_block_E):
    line_bot_api = LineBotApi(channel_access_token)
    S_list = []
    E_list = []
    for i in range(0, min(3, len(kouho_block_S))):
        S_list.append(PostbackTemplateAction(
            label=kouho_block_S[i],
            #text='postback text1',
            data=kouho_block_S[i] + 'station1'
        ))

    for i in range(0, min(3, len(kouho_block_E))):
        E_list.append(PostbackTemplateAction(
            label=kouho_block_E[i],
            #text='postback text1',
            data=kouho_block_E[i] + 'station2'
        ))

    for i in range(0, 3):
        if(len(S_list) < 3):
            S_list.append(PostbackTemplateAction(
                label="-",
                #text='postback text1',
                data='none'
            ))
        else:
            break
    for i in range(0, 3):
        if(len(E_list) < 3):
            E_list.append(PostbackTemplateAction(
                label="-",
                #text='postback text1',
                data='none'
            ))
        else:
            break

    Carousel_template = TemplateSendMessage(
        alt_text='請輸入確切的起迄站名。',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://www.jorudan.co.jp/com/img/bnr/ogp_jorudan.png',
                    title="請問你的起站是?",
                    text=eki_S,
                    actions=S_list
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.jorudan.co.jp/com/img/bnr/ogp_jorudan.png',
                    title="請問你的迄站是?",
                    text=eki_E,
                    actions=E_list
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, Carousel_template)
    return "OK"


"""
@handler.add(PostbackEvent)
def handle_post_message(event):
    dateTime = event.postback.Params.DateTime
    print(f"{dateTime}")
"""

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
