# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# ======這裡是呼叫的自定義的函式=====
from message import *
from new import *
from Function import *
# ======這裡是呼叫的自定義的函式=====

# ======這裡是呼叫資料庫=====
import db
import json
with open('events.json', mode='r', encoding='utf-8') as f:
    events = json.load(f)
# ======這裡是呼叫資料庫=====


# ======python的函數庫==========
import tempfile
import os
import datetime
from urllib.parse import parse_qsl
import random
# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# LINE Bot: WALL-E
line_bot_api = LineBotApi(
    'I5hgulT9ZKbbAFqbzumFaVYS0jgUmuyG5JVmFgrq+HlPngNiK05bfvgsiBzAxOAjwE3FAc5olRj+iXwglbNuz6Qpp0YAW9z/Mq72Ea+96SzEMbp6KChDbEg74sa4c433HzVMB59OUPcK45d9l6n1uQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('be58b1568a2dbd2327a5c6f6bd48e80a')


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
    elif '華山在哪裡' == msg:
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
    elif '松菸在哪裡' == msg:
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
    elif '展覽表演' == msg:
        try:
            # 選擇四個隨機活動
            rand_nums = random.sample(range(len(events)), 4)
            reply_message = TemplateSendMessage(
                alt_text='Carousel Template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=events[rand_nums[0]]['image'],
                            title=events[rand_nums[0]]['title'][:20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
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
    elif '品牌活動' == msg:
        try:
            reply_message = TemplateSendMessage(
                alt_text='一則旋轉木馬按鈕訊息',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30' + '\n' +
                            'Underground River——由 iDrip 主策劃的 #暗通款曲 快閃餐 Bar，以風味交流為題，宛如伏流般讓各股風味在此幽會，此交會融合，深刻、神秘、迷人又致命。iDrip 集結世界冠軍與茶、咖啡大師的手藝及選材，佐以米其林一星餐館——大三元酒樓一甲子的精湛廚藝，並於每月 cross 全台口碑甜點，伴隨著霓虹蕩漾、風情萬種會聚一溏，進入時而細緻、忽而彩麗的體驗，展現各方精湛、令人窒息的偷情魅力。'[
                                :40] + '…',
                            actions=[
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
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
    elif '論壇講座' == msg:
        try:
            reply_message = TemplateSendMessage(
                alt_text='Carousel Template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30',
                            actions=[
                                PostbackTemplateAction(
                                    label='回傳一個訊息',
                                    data='將這個訊息偷偷回傳給機器人'
                                ),
                                MessageTemplateAction(
                                    label='用戶發送訊息',
                                    text='我知道這是1'
                                ),
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/0530%20ClaireBN_21042114540500753.jpg',
                            title='Claire老師《超認真英文課》'[:20],
                            text='2021.05.30',
                            actions=[
                                PostbackTemplateAction(
                                    label='回傳一個訊息',
                                    data='這是ID=2'
                                ),
                                MessageTemplateAction(
                                    label='用戶發送訊息',
                                    text='我知道這是2'
                                ),
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21042114510611337'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%ae%80%e8%a1%a3%e8%a8%88%e7%95%ab_DD_Banner_1920x1080px_Finished%20File_20210416-1.jpg',
                            title='讀衣V藝術時尚跨界展'[:20],
                            text='2021.05.08 - 05.23',
                            actions=[
                                PostbackTemplateAction(
                                    label='回傳一個訊息',
                                    data='這是ID=3'
                                ),
                                MessageTemplateAction(
                                    label='用戶發送訊息',
                                    text='我知道這是3'
                                ),
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21042218335496536'
                                )
                            ]
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
    elif '市集活動' == msg:
        try:
            reply_message = TemplateSendMessage(
                alt_text='一則旋轉木馬按鈕訊息',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%8f%af%e5%b1%b1_%e4%b8%bb%e9%a0%81%e6%9b%9d%e5%85%89.jpg',
                            title='暗通款曲 快閃餐吧 Underground River Pop-up Deli & Bar'[
                                :20],
                            text='2021.05.18 - 07.30',
                            actions=[
                                PostbackTemplateAction(
                                    label='回傳一個訊息',
                                    data='將這個訊息偷偷回傳給機器人'
                                ),
                                MessageTemplateAction(
                                    label='用戶發送訊息',
                                    text='我知道這是1'
                                ),
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21052211510176911'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/0530%20ClaireBN_21042114540500753.jpg',
                            title='Claire老師《超認真英文課》'[:20],
                            text='2021.05.30',
                            actions=[
                                PostbackTemplateAction(
                                    label='回傳一個訊息',
                                    data='這是ID=2'
                                ),
                                MessageTemplateAction(
                                    label='用戶發送訊息',
                                    text='我知道這是2'
                                ),
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21042114510611337'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://media.huashan1914.com/WebUPD/huashan1914/exhibition/%e8%ae%80%e8%a1%a3%e8%a8%88%e7%95%ab_DD_Banner_1920x1080px_Finished%20File_20210416-1.jpg',
                            title='讀衣V藝術時尚跨界展'[:20],
                            text='2021.05.08 - 05.23',
                            actions=[
                                PostbackTemplateAction(
                                    label='回傳一個訊息',
                                    data='這是ID=3'
                                ),
                                MessageTemplateAction(
                                    label='用戶發送訊息',
                                    text='我知道這是3'
                                ),
                                URITemplateAction(
                                    label='進入活動頁面',
                                    uri='https://www.huashan1914.com//w/huashan1914/exhibition_21042218335496536'
                                )
                            ]
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
                text='文字訊息為「@隨機推薦」的動作'
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
    # 測試測試測試測試測試測試
    elif '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    # 無法辨識使用者的訊息
    else:
        reply_message = TextSendMessage(
            text="你說的話是：「" + msg + "」，目前無法辨識此訊息。"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)


@handler.add(PostbackEvent)  # PostbackTemplateAction 觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  # 取得 data 資料
    if backdata.get('action') == 'sell':  # 讀取 Postback 資料中名稱為「action」項目的值
        reply_message = sendData_sell(event, backdata)
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif backdata.get('action') == 'xxx':
        reply_message = TextSendMessage(
            text='呼叫後台成功'
        )
        line_bot_api.reply_message(event.reply_token, reply_message)


# 回傳 postback 資料
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
                        initial=str(datetime.date.today()),  # 顯示初始日期
                        min="2020-10-01",  # 最小日期
                        max="2021-12-31"  # 最大日期
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


def sendData_sell(event, backdata):
    try:
        if backdata.get('mode') == 'date':
            reply_message = TextSendMessage(
                text='日期為：' + event.postback.params.get('date') + '，找尋當天的活動'
            )
            return reply_message
    except:
        reply_message = TextSendMessage(
            text='發生錯誤！'
        )
        return reply_message


if __name__ == '__main__':  # 如果此程式碼檔案被直接執行（而非被其他檔案 import）的話，就執行以下敘述。
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
