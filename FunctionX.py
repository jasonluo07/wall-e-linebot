# 這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import datetime


def send_datetime():
    message = TemplateSendMessage(
        alt_text='日期時間範例',
        template=ButtonsTemplate(
            thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
            title="日期時間範例",
            text="請選擇",
            actions=[
                DatetimePickerTemplateAction(
                    label="選擇時間",
                    data="input_birthday",
                    mode='date',
                    initial='2021-01-01',  # 待完成功能：初始時間要同步更新至今日
                    max='2021-12-31',
                    min='2021-01-01'
                )
            ]
        )
    )
    return message
