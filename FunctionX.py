'''
# 這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import datetime


def sendDatetime():
    message = TemplateSendMessage(
        alt_text='日期時間範例',
        
    )
'''
