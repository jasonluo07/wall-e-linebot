from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile
import os
import datetime
import time
# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'I5hgulT9ZKbbAFqbzumFaVYS0jgUmuyG5JVmFgrq+HlPngNiK05bfvgsiBzAxOAjwE3FAc5olRj+iXwglbNuz6Qpp0YAW9z/Mq72Ea+96SzEMbp6KChDbEg74sa4c433HzVMB59OUPcK45d9l6n1uQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('be58b1568a2dbd2327a5c6f6bd48e80a')

# 監聽所有來自 /callback 的 Post Request


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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '華山' in msg:
        reply_message = LocationSendMessage(
            title="華山",
            address="華山1914文化創意產業園區",
            latitude="25.0442906858476",
            longitude="121.52934759683569"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '松菸' in msg:
        reply_message = LocationSendMessage(
            title="松菸",
            address="松山文創園區",
            latitude="25.04402152155643",
            longitude="121.5606831170937"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif '測試' == msg:
        reply_message = TextMessage(text='測試成功')
        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )
    else:
        reply_message = TextSendMessage(text="你說的話是：" + msg "，目前無法辨識此訊息。")
        line_bot_api.reply_message(event.reply_token, reply_message)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
