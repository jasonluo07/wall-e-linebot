from flask import Flask
from flask import request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *


# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
from FunctionX import *
import db
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile
import os
import datetime
import time
from urllib.parse import parse_qsl
import random
# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# 設定 Channel Access Token 及 Channel Secret 資訊
line_bot_api = LineBotApi(
    'I5hgulT9ZKbbAFqbzumFaVYS0jgUmuyG5JVmFgrq+HlPngNiK05bfvgsiBzAxOAjwE3FAc5olRj+iXwglbNuz6Qpp0YAW9z/Mq72Ea+96SzEMbp6KChDbEg74sa4c433HzVMB59OUPcK45d9l6n1uQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('be58b1568a2dbd2327a5c6f6bd48e80a')

# 實裝中


def sendDatetime(event):  # 日期時間
    try:
        reply_message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",  # 觸發postback事件
                        mode="date",  # 選取日期
                        initial="2020-10-01",  # 顯示初始日期
                        min="2020-10-01",  # 最小日期
                        max="2021-12-31"  # 最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell&mode=time",
                        mode="time",  # 選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell&mode=datetime",
                        mode="datetime",  # 選取日期時間
                        initial="2020-10-01T10:00",
                        min="2020-10-01T00:00",
                        max="2021-12-31T23:59"
                    )
                ]
            )
        )
        return reply_message
    except:
        reply_message = TextSendMessage(
            text='發生錯誤！'
        )
        return reply_message


def sendData_sell(event, backdata):  # Postback,顯示日期時間
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')  # 讀取日期
        elif backdata.get('mode') == 'time':
            dt = '時間為：' + event.postback.params.get('time')  # 讀取時間
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get(
                'datetime'), '%Y-%m-%dT%H:%M')  # 讀取日期時間
            dt = dt.strftime(
                '{d}%Y-%m-%d, {t}%H:%M').format(d='日期為：', t='時間為：')  # 轉為字串
        reply_message = TextSendMessage(
            text=dt
        )
        return reply_message
    except:
        reply_message = TextSendMessage(
            text='發生錯誤！'
        )
        return reply_message


# 建立 callback 路由，檢查 LINE Bot 的資訊是否正確
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
# 回應訊息（reply_message）的種類有 Text（文字）、Image（圖片）、Location（位置）、Sticker（貼圖）、Audio（聲音）、Video（影片）、Template（樣板）等
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text  # 使用者傳送的文字
    # 處理文字訊息的部分
    if '你好' == msg:
        try:
            reply_message = TextSendMessage(
                text='我是瓦力，\n你好！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '華山' == msg:
        try:
            reply_message = LocationSendMessage(
                title="華山1914文化創意產業園區",
                address="台北市中正區八德路一段1號",
                latitude="25.0442906858476",
                longitude="121.52934759683569"
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '松菸' == msg:
        try:
            reply_message = LocationSendMessage(
                title="松山文創園區",
                address="台北市信義區光復南路133號",
                latitude="25.04402152155643",
                longitude="121.5606831170937"
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    # 處理圖文選單的部分
    elif '@時間' == msg:
        try:
            reply_message = sendDatetime(event)
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        # 待加上功能：回傳使用者選擇的日期時間
    elif '@類別' == msg:  # "quick reply buttons": https://pse.is/3h5spb
        try:
            reply_message = TextSendMessage(
                text='請選擇以下類別',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='展覽表演',  # 「顯示值」是顯示於快速選單的文字
                                text='展覽表演'  # 「選取值」是使用者選按該選項回傳的文字
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='品牌活動',
                                text='品牌活動'
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='論壇講座',
                                text='論壇講座'
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='市集活動',
                                text='市集活動'
                            )
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '@隨機推薦' == msg:
        try:
            reply_message = TextSendMessage(
                text='顯示「@隨機推薦」的動作'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '@笑一下' == msg:
        try:
            reply_message = ImageSendMessage(
                original_content_url=db.memestw[random.randrange(
                    len(db.memestw))],
                preview_image_url=db.memestw[random.randrange(len(db.memestw))]
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='「笑一下」發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    #
    #
    # 範例測試
    #
    #
    #
    #
    # 測試功能列表＋隨機推薦
    elif '隨機推薦' == msg:
        reply_message = function_list()
        line_bot_api.reply_message(event.reply_token, reply_message)
    # 測試用功能
    elif '最新合作廠商' == msg:
        reply_message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '旋轉木馬' == msg:
        reply_message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '旋轉木馬2' == msg:
        reply_message = image_carousel_message1()
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '按鈕' == msg:
        reply_message = buttons_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
    # 無法辨識使用者的訊息
    else:
        reply_message = TextSendMessage(
            text="你說的話是：「" + msg + "」，目前無法辨識此訊息。"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)


def sendDatetime(event):  # 日期時間
    try:
        reply_message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",  # 觸發postback事件
                        mode="date",  # 選取日期
                        initial="2020-10-01",  # 顯示初始日期
                        min="2020-10-01",  # 最小日期
                        max="2021-12-31"  # 最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell&mode=time",
                        mode="time",  # 選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell&mode=datetime",
                        mode="datetime",  # 選取日期時間
                        initial="2020-10-01T10:00",
                        min="2020-10-01T00:00",
                        max="2021-12-31T23:59"
                    )
                ]
            )
        )
        return reply_message
    except:
        reply_message = TextSendMessage(
            text='發生錯誤！'
        )
        return reply_message


def sendData_sell(event, backdata):  # Postback,顯示日期時間
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')  # 讀取日期
        elif backdata.get('mode') == 'time':
            dt = '時間為：' + event.postback.params.get('time')  # 讀取時間
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get(
                'datetime'), '%Y-%m-%dT%H:%M')  # 讀取日期時間
            dt = dt.strftime(
                '{d}%Y-%m-%d, {t}%H:%M').format(d='日期為：', t='時間為：')  # 轉為字串
        reply_message = TextSendMessage(
            text=dt
        )
        return reply_message
    except:
        reply_message = TextSendMessage(
            text='發生錯誤！'
        )
        return reply_message


# 日期時間按鈕會觸發 Postback 事件
@handler.add(PostbackEvent)  # PostbackTemplateAction 觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  # 取得 data 資料
    if backdata.get('action') == 'sell':  # 讀取 Postback 資料中名稱為「action」項目的值
        sendData_sell(event, backdata)


if __name__ == '__main__':  # 如果此程式碼檔案被直接執行（而非被其他檔案 import）的話，就執行以下敘述。
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
