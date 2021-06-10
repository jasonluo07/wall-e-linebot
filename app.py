# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# ======python的函數庫==========
import tempfile
import os
import datetime
from datetime import date
import random
from urllib.parse import parse_qsl
import json
# ======python的函數庫==========

# ======這裡是呼叫的自定義的函式=====
from message import *
from new import *
from Function import *
# ======這裡是呼叫的自定義的函式=====

# ======這裡是呼叫資料庫=====
import db
with open('./web_crawler/memestw.json', mode='r', encoding='utf-8') as file:
    memestw = json.load(file)
# ======這裡是呼叫資料庫=====


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# LINE Bot: WALL-E
line_bot_api = LineBotApi(
    'I5hgulT9ZKbbAFqbzumFaVYS0jgUmuyG5JVmFgrq+HlPngNiK05bfvgsiBzAxOAjwE3FAc5olRj+iXwglbNuz6Qpp0YAW9z/Mq72Ea+96SzEMbp6KChDbEg74sa4c433HzVMB59OUPcK45d9l6n1uQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('be58b1568a2dbd2327a5c6f6bd48e80a')
# LINE Bot: testbot371
# line_bot_api = LineBotApi(
#     'pI2RMOmFid7t4LcAXLD6xtINIdt1GTk47SV+/3VObyfqrnEO+OVv/1NiJGDmv5nldjF6fzXrwZ+uMie+Hil5rjD1UhstcCOYtNrOuR0b5OXWIKEt1L7D83YlWEaRRwSw39lUY9CxEzpqeduShuc6EQdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('0583d8005933cf8d466126a3649b1952')


# 建立 callback 路由，檢查 LINE Bot 的資訊是否正確
@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
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
    # 處理圖文選單的部分
    elif '@日期' == msg:
        try:
            reply_message = send_datetime(event)
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '@類別' == msg:  # "quick reply buttons": https://pse.is/3h5spb
        try:
            reply_message = TextSendMessage(
                text='請選擇以下類別',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='展覽活動',  # 「顯示值」是顯示於快速選單的文字
                                text='展覽活動'  # 「選取值」是使用者選按該選項回傳的文字
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='表演活動',
                                text='表演活動'
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
    elif '展覽活動' == msg:
        try:
            reply_message = pick_random_events(db.eventsT, target_type='展覽活動')
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='目前沒有展覽表演'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '表演活動' == msg:
        try:
            reply_message = pick_random_events(db.eventsT, target_type='表演活動')
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='目前沒有表演活動！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '品牌活動' == msg:
        try:
            reply_message = pick_random_events(db.eventsT, target_type='品牌活動')
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='目前沒有品牌活動！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '論壇講座' == msg:
        try:
            reply_message = pick_random_events(db.eventsT, target_type='論壇講座')
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='目前沒有論壇講座！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '@地點' == msg:
        try:
            reply_message = TextSendMessage(
                text='請選擇以下地點',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='華山在哪',
                                text='華山在哪'
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='松菸在哪',
                                text='松菸在哪'
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='北美館在哪',
                                text='北美館在哪'
                            )
                        ),
                        QuickReplyButton(
                            action=MessageAction(
                                label='中正紀念堂在哪',
                                text='中正紀念堂在哪'
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
    elif '華山在哪' in msg:
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
    elif '松菸在哪' in msg:
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
    elif '北美館在哪' in msg:
        try:
            reply_message = LocationSendMessage(
                title="臺北市立美術館",
                address="台北市中山區中山北路三段181號",
                latitude="25.07258670583647",
                longitude="121.52487457050282"
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '中正紀念堂在哪' in msg:
        try:
            reply_message = LocationSendMessage(
                title="中正紀念堂",
                address="台北市中正區中山南路21號",
                latitude="25.034771233006982",
                longitude="121.52175635037176"
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    elif '@笑一下' == msg:
        try:
            image_url = memestw[random.randrange(len(memestw))]
            reply_message = ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
        except:
            reply_message = TextSendMessage(
                text='發生錯誤！'
            )
            line_bot_api.reply_message(event.reply_token, reply_message)
    # 無法辨識使用者的訊息
    else:
        reply_message = TextSendMessage(
            text="瓦力無法各別回覆，請輸入關鍵字，如：「展覽活動」、「華山在哪裡」等。"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)


@handler.add(PostbackEvent)  # PostbackTemplateAction 觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  # 取得 data 資料
    if backdata.get('action') == 'sell':  # 讀取 Postback 資料中名稱為「action」項目的值
        reply_message = send_data_sell(event, backdata)
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif backdata.get('action') == 'xxx':
        reply_message = TextSendMessage(
            text='呼叫後台成功'
        )
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif backdata.get('action') == 'again':
        reply_message = pick_random_events(db.eventsT)  # db.eventsT 要換
        line_bot_api.reply_message(event.reply_token, reply_message)


# 回傳 postback 資料
def send_datetime(event):  # 日期時間
    try:
        reply_message = TemplateSendMessage(
            alt_text='選擇日期',
            template=ButtonsTemplate(
                # thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='選擇日期',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",  # 觸發postback事件
                        mode="date",  # 選取日期
                        initial=str(datetime.date.today()),  # 顯示初始日期
                        min=str(datetime.date.today() - \
                                datetime.timedelta(days=730)),  # 最小日期
                        max=str(datetime.date.today() + \
                                datetime.timedelta(days=730))  # 最大日期
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


def send_data_sell(event, backdata):
    try:
        if backdata.get('mode') == 'date':
            # reply_message = TextSendMessage(
            #     text='日期為：' + event.postback.params.get('date') + '，找尋當天的活動'
            # )
            reply_message = pick_random_events(db.eventsT)
            return reply_message
    except:
        reply_message = TextSendMessage(
            text='發生錯誤！'
        )
        return reply_message


def pick_random_events(data, target_date=str(datetime.date.today()), target_type='不限', target_place='不限'):
    target_events = []
    target_date = date.fromisoformat(target_date.replace('.', '-'))

    # 篩選資料
    if target_type != '不限' & target_place != '不限':
        for i in range(len(data)):
            start_date = date.fromisoformat(
                data[i]['beginDate'].replace('.', '-'))
            end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
            boolean1 = (start_date <= target_date <= end_date)
            boolean2 = (target_type == data[i]['type'])
            boolean3 = (target_place == data[i]['location'])
            if boolean1 & boolean2 & boolean3:  # 日期 & 類型 & 地點
                target_events.append(data[i])
    elif target_type == '不限' & target_place != '不限':
        for i in range(len(data)):
            start_date = date.fromisoformat(
                data[i]['beginDate'].replace('.', '-'))
            end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
            boolean1 = (start_date <= target_date <= end_date)
            boolean3 = (target_place == data[i]['location'])
            if boolean1 & boolean3:  # 日期 & 地點
                target_events.append(data[i])
    elif target_type != '不限' & target_place == '不限':
        for i in range(len(data)):
            start_date = date.fromisoformat(
                data[i]['beginDate'].replace('.', '-'))
            end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
            boolean1 = (start_date <= target_date <= end_date)
            boolean2 = (target_type == data[i]['type'])
            if boolean1 & boolean2:  # 日期 & 類型
                target_events.append(data[i])
    elif target_type == '不限' & target_place == '不限':
        for i in range(len(data)):
            start_date = date.fromisoformat(
                data[i]['beginDate'].replace('.', '-'))
            end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
            boolean1 = (start_date <= target_date <= end_date)
            if boolean1:  # 日期
                target_events.append(data[i])

    # 隨機抓取篩選過後的資料
    # 三種狀況：(1) 大於等於 3，(2) 等於 2，(3) 等於 1，(4) 等於 0
    if len(target_events) >= 3:
        rand_nums = random.sample(range(len(target_events)), 3)
        event1 = events[rand_nums[0]]
        event2 = events[rand_nums[1]]
        event3 = events[rand_nums[2]]
        reply_message = TemplateSendMessage(
            alt_text='Carousel Template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=event1['image'],
                        title=event1['title'][:20],
                        text=event1['beginDate'] + ' - ' + event1['endDate'].replace(
                            '2021.', '').replace('2020.', '') + ' ' + event1['location'] + '\n' + event1['description'][:25] + '…',
                        actions=[
                            URITemplateAction(
                                label='進入活動頁面',
                                uri=event1['href']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=event2['image'],
                        title=event2['title'][:20],
                        text=event2['beginDate'] + ' - ' + event2['endDate'].replace(
                            '2021.', '').replace('2020.', '') + ' ' + event2['location'] + '\n' + event2['description'][:25] + '…',
                        actions=[
                            URITemplateAction(
                                label='進入活動頁面',
                                uri=event2['href']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=event3['image'],
                        title=event3['title'][:20],
                        text=event3['beginDate'] + ' - ' + event3['endDate'].replace(
                            '2021.', '').replace('2020.', '') + ' ' + event3['location'] + '\n' + event3['description'][:25] + '…',
                        actions=[
                            URITemplateAction(
                                label='進入活動頁面',
                                uri=event3['href']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/lpnJaXe.jpg',
                        title='換下一組',
                        text='換下一組',
                        actions=[
                            PostbackTemplateAction(
                                label='換下一組',
                                data='action=again'
                            )
                        ]
                    )
                ]
            )
        )
    elif len(target_events) == 2:
        rand_nums = random.sample(range(len(target_events)), 2)
        event1 = events[rand_nums[0]]
        event2 = events[rand_nums[1]]
        reply_message = TemplateSendMessage(
            alt_text='Carousel Template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=event1['image'],
                        title=event1['title'][:20],
                        text=event1['beginDate'] + ' - ' + event1['endDate'].replace(
                            '2021.', '').replace('2020.', '') + ' ' + event1['location'] + '\n' + event1['description'][:25] + '…',
                        actions=[
                            URITemplateAction(
                                label='進入活動頁面',
                                uri=event1['href']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=event2['image'],
                        title=event2['title'][:20],
                        text=event2['beginDate'] + ' - ' + event2['endDate'].replace(
                            '2021.', '').replace('2020.', '') + ' ' + event2['location'] + '\n' + event2['description'][:25] + '…',
                        actions=[
                            URITemplateAction(
                                label='進入活動頁面',
                                uri=event2['href']
                            )
                        ]
                    )
                ]
            )
        )
    elif len(target_events) == 1:
        rand_nums = random.sample(range(len(target_events)), 1)
        event1 = events[rand_nums[0]]
        reply_message = TemplateSendMessage(
            alt_text='Carousel Template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=event1['image'],
                        title=event1['title'][:20],
                        text=event1['beginDate'] + ' - ' + event1['endDate'].replace(
                            '2021.', '').replace('2020.', '') + ' ' + event1['location'] + '\n' + event1['description'][:25] + '…',
                        actions=[
                            URITemplateAction(
                                label='進入活動頁面',
                                uri=event1['href']
                            )
                        ]
                    )
                ]
            )
        )
    elif len(target_events) >= 0:
        reply_message = TextSendMessage(
            text='沒有活動了！'
        )
    return reply_message


if __name__ == '__main__':  # 如果此程式碼檔案被直接執行（而非被其他檔案 import）的話，就執行以下敘述。
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
