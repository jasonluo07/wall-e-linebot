# 這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import datetime
import time
from urllib import parse_qsl


def sendDatetime(event):  # 日期時間
    try:
        message = TemplateSendMessage(
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
                        initial=time.strftime("%Y-%m-%d"),  # 顯示初始日期
                        min="2020-10-01",  # 最小日期
                        max="2021-12-31"  # 最大日期
                    )
                ]
            )
        )
        return message
    except:
        message = '發生錯誤！'
        return message


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
        message = TextSendMessage(
            text=dt
        )
        return message
    except:
        message = '發生錯誤！'
        return message


'''
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
'''
