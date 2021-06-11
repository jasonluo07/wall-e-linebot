# ===============這些是LINE提供的功能套組，先用import叫出來=============
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
# ===============LINEAPI=============================================

import datetime
from datetime import date
import random
import json


def pick_random_activities2(activities):
    target_date = datetime.date.today()
    activitiesA = []
    for i in range(len(activities)):
        type = activities[i]['type']
        start_date = date.fromisoformat(
            activities[i]['startDate'].replace('.', '-'))
        end_date = date.fromisoformat(
            activities[i]['endDate'].replace('.', '-'))
        boolean1 = type == '展覽活動'
        boolean2 = start_date <= target_date <= end_date
        if boolean1 & boolean2:
            activitiesA.append(activities[i])

    rand_nums = random.sample(range(len(activitiesA)), 3)
    activity1 = activitiesA[rand_nums[0]]
    activity2 = activitiesA[rand_nums[1]]
    activity3 = activitiesA[rand_nums[2]]
    reply_message = TemplateSendMessage(
        alt_text='Carousel Template',
        template=CarouselTemplate(
            columns=[
                 CarouselColumn(
                     thumbnail_image_url=activity1['image'],
                     title=activity1['title'][:20],
                     text=activity1['startDate'] + ' - ' + activity1['endDate'].replace(
                         '2021.', '').replace('2020.', '').replace('2019.', '').replace('2018.', '') + ' ' + activity1['location'] + '\n' + activity1['description'][:25] + '…',
                     actions=[
                         URITemplateAction(
                             label='進入活動頁面',
                             uri=activity1['href']
                         )
                     ]
                 ),
                CarouselColumn(
                     thumbnail_image_url=activity2['image'],
                     title=activity2['title'][:20],
                     text=activity2['startDate'] + ' - ' + activity2['endDate'].replace(
                         '2021.', '').replace('2020.', '').replace('2019.', '').replace('2018.', '') + ' ' + activity2['location'] + '\n' + activity2['description'][:25] + '…',
                     actions=[
                         URITemplateAction(
                             label='進入活動頁面',
                             uri=activity2['href']
                         )
                     ]
                 ),
                CarouselColumn(
                     thumbnail_image_url=activity3['image'],
                     title=activity3['title'][:20],
                     text=activity3['startDate'] + ' - ' + activity3['endDate'].replace(
                         '2021.', '').replace('2020.', '').replace('2019.', '').replace('2018.', '') + ' ' + activity3['location'] + '\n' + activity3['description'][:25] + '…',
                     actions=[
                         URITemplateAction(
                             label='進入活動頁面',
                             uri=activity3['href']
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
    return reply_message


# pick_random_events2(activities)
# def pick_random_events2(data, target_date=str(datetime.date.today()).replace('-', '.'), target_type='不限', target_place='不限'):
#     target_events = []
#     target_date = date.fromisoformat(target_date.replace('.', '-'))

#     # 篩選資料
#     if target_type != '不限' & target_place != '不限':
#         for i in range(len(data)):
#             start_date = date.fromisoformat(
#                 data[i]['startDate'].replace('.', '-'))
#             end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
#             boolean1 = (start_date <= target_date <= end_date)
#             boolean2 = (target_type == data[i]['type'])
#             boolean3 = (target_place == data[i]['location'])
#             if boolean1 & boolean2 & boolean3:  # 日期 & 類型 & 地點
#                 target_events.append(data[i])
#     elif target_type == '不限' & target_place != '不限':
#         for i in range(len(data)):
#             start_date = date.fromisoformat(
#                 data[i]['startDate'].replace('.', '-'))
#             end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
#             boolean1 = (start_date <= target_date <= end_date)
#             boolean3 = (target_place == data[i]['location'])
#             if boolean1 & boolean3:  # 日期 & 地點
#                 target_events.append(data[i])
#     elif target_type != '不限' & target_place == '不限':
#         for i in range(len(data)):
#             start_date = date.fromisoformat(
#                 data[i]['startDate'].replace('.', '-'))
#             end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
#             boolean1 = (start_date <= target_date <= end_date)
#             boolean2 = (target_type == data[i]['type'])
#             if boolean1 & boolean2:  # 日期 & 類型
#                 target_events.append(data[i])
#     elif target_type == '不限' & target_place == '不限':
#         for i in range(len(data)):
#             start_date = date.fromisoformat(
#                 data[i]['startDate'].replace('.', '-'))
#             end_date = date.fromisoformat(data[i]['endDate'].replace('.', '-'))
#             boolean1 = (start_date <= target_date <= end_date)
#             if boolean1:  # 日期
#                 target_events.append(data[i])

#     # 隨機抓取篩選過後的資料
#     # 三種狀況：(1) 大於等於 3，(2) 等於 2，(3) 等於 1，(4) 等於 0
#     if len(target_events) >= 3:
#         rand_nums = random.sample(range(len(target_events)), 3)
#         activity1 = target_events[rand_nums[0]]
#         activity2 = target_events[rand_nums[1]]
#         activity3 = target_events[rand_nums[2]]
#         reply_message = TemplateSendMessage(
#             alt_text='Carousel Template',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url=activity1['image'],
#                         title=activity1['title'][:20],
#                         text=activity1['startDate'] + ' - ' + activity1['endDate'].replace(
#                             '2021.', '').replace('2020.', '') + ' ' + activity1['location'] + '\n' + activity1['description'][:25] + '…',
#                         actions=[
#                             URITemplateAction(
#                                 label='進入活動頁面',
#                                 uri=activity1['href']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=activity2['image'],
#                         title=activity2['title'][:20],
#                         text=activity2['startDate'] + ' - ' + activity2['endDate'].replace(
#                             '2021.', '').replace('2020.', '') + ' ' + activity2['location'] + '\n' + activity2['description'][:25] + '…',
#                         actions=[
#                             URITemplateAction(
#                                 label='進入活動頁面',
#                                 uri=activity2['href']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=activity3['image'],
#                         title=activity3['title'][:20],
#                         text=activity3['startDate'] + ' - ' + activity3['endDate'].replace(
#                             '2021.', '').replace('2020.', '') + ' ' + activity3['location'] + '\n' + activity3['description'][:25] + '…',
#                         actions=[
#                             URITemplateAction(
#                                 label='進入活動頁面',
#                                 uri=activity3['href']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url='https://i.imgur.com/lpnJaXe.jpg',
#                         title='換下一組',
#                         text='換下一組',
#                         actions=[
#                             PostbackTemplateAction(
#                                 label='換下一組',
#                                 data='action=again'
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#     elif len(target_events) == 2:
#         rand_nums = random.sample(range(len(target_events)), 2)
#         activity1 = target_events[rand_nums[0]]
#         activity2 = target_events[rand_nums[1]]
#         reply_message = TemplateSendMessage(
#             alt_text='Carousel Template',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url=activity1['image'],
#                         title=activity1['title'][:20],
#                         text=activity1['startDate'] + ' - ' + activity1['endDate'].replace(
#                             '2021.', '').replace('2020.', '') + ' ' + activity1['location'] + '\n' + activity1['description'][:25] + '…',
#                         actions=[
#                             URITemplateAction(
#                                 label='進入活動頁面',
#                                 uri=activity1['href']
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnail_image_url=activity2['image'],
#                         title=activity2['title'][:20],
#                         text=activity2['startDate'] + ' - ' + activity2['endDate'].replace(
#                             '2021.', '').replace('2020.', '') + ' ' + activity2['location'] + '\n' + activity2['description'][:25] + '…',
#                         actions=[
#                             URITemplateAction(
#                                 label='進入活動頁面',
#                                 uri=activity2['href']
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#     elif len(target_events) == 1:
#         rand_nums = random.sample(range(len(target_events)), 1)
#         activity1 = target_events[rand_nums[0]]
#         reply_message = TemplateSendMessage(
#             alt_text='Carousel Template',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url=activity1['image'],
#                         title=activity1['title'][:20],
#                         text=activity1['startDate'] + ' - ' + activity1['endDate'].replace(
#                             '2021.', '').replace('2020.', '') + ' ' + activity1['location'] + '\n' + activity1['description'][:25] + '…',
#                         actions=[
#                             URITemplateAction(
#                                 label='進入活動頁面',
#                                 uri=activity1['href']
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#     elif len(target_events) == 0:
#         reply_message = TextSendMessage(
#             text='沒有活動了！'
#         )
#     return reply_message
