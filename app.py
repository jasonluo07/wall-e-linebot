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
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile
import os
import datetime
import time
from urllib.parse import parse_qsl
# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# 設定 Channel Access Token 及 Channel Secret 資訊
line_bot_api = LineBotApi(
    'I5hgulT9ZKbbAFqbzumFaVYS0jgUmuyG5JVmFgrq+HlPngNiK05bfvgsiBzAxOAjwE3FAc5olRj+iXwglbNuz6Qpp0YAW9z/Mq72Ea+96SzEMbp6KChDbEg74sa4c433HzVMB59OUPcK45d9l6n1uQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('be58b1568a2dbd2327a5c6f6bd48e80a')


# 建立 callback 路由，檢查 LINE Bot 的資訊是否正確
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
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
    # 是否正運行
    if '測試2' == msg:
        reply_message = TextSendMessage(text='測試成功2，程式正常運作')
        line_bot_api.reply_message(event.reply_token, reply_message)
    # 回傳文字
    elif '@日期時間' == msg:
        reply_message = sendDatetime(event)
        line_bot_api.reply_message(
            event.reply_token, reply_message)  # 待加上功能：回傳使用者選擇的日期時間
    # 回傳樣板訊息
    elif '近期活動' == msg:
        reply_message = TextSendMessage(text='顯示近期活動')
        line_bot_api.reply_message(event.reply_token, reply_message)
    # 類別選項
    elif '類別' == msg:
        reply_message = TextSendMessage(
            text='請選擇以下類別並輸入編號：\n1. 展覽表演\n2. 品牌活動\n3. 論壇講座\n4. 市集活動')
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '1' == msg[0]:
        reply_message = TextSendMessage(text='我是展覽表演')
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '2' == msg[0]:
        reply_message = TextSendMessage(text='我是品牌活動')
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '3' == msg[0]:
        reply_message = TextSendMessage(text='我是論壇講座')
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '4' == msg[0]:
        reply_message = TextSendMessage(text='我是市集活動')
        line_bot_api.reply_message(event.reply_token, reply_message)
    # 回傳位置訊息
    elif '華山' == msg:
        reply_message = LocationSendMessage(
            title="華山1914文化創意產業園區",
            address="台北市中正區八德路一段1號",
            latitude="25.0442906858476",
            longitude="121.52934759683569"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '松菸' == msg:
        reply_message = LocationSendMessage(
            title="松山文創園區",
            address="台北市信義區光復南路133號",
            latitude="25.04402152155643",
            longitude="121.5606831170937"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
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
    # 開發中的功能
    elif '@傳送圖片' == msg:
        reply_message = ImageSendMessage(
            original_content_url="https://i.imgur.com/NY2RqSD.png",
            preview_image_url="https://i.imgur.com/NY2RqSD.png"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    # 無法辨識使用者的訊息
    else:
        reply_message = TextSendMessage(text="你說的話是：" + msg + "，目前無法辨識此訊息。")
        line_bot_api.reply_message(event.reply_token, reply_message)

# 日期時間按鈕會觸發 Postback 事件


@handler.add(PostbackEvent)  # PostbackTemplateAction觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  # 取得data資料
    if backdata.get('action') == 'sell':
        sendData_sell(event, backdata)


if __name__ == '__main__':  # 如果此程式碼檔案被直接執行（而非被其他檔案 import）的話，就執行以下敘述。
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
