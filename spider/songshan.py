import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from datetime import date


def get_songshan_exhibition(url, kind, type):
    # 判斷爬取日期
    date_A = datetime.date.today() - datetime.timedelta(days=1095)

    data = []
    page = 1

    while True:
        print(f"正在爬取第 {page} 頁")
        my_params = {'kind': kind, 'type': type, 'p': page, 'q': 'get'}
        resp = requests.get(url, params=my_params)
        divs = json.loads(resp.text)['items']  # list 物件
        if not divs:  # divs 為空
            break

        # 整理 json 格式
        for d in divs:
            try:
                title = d['Title'].strip()
                image = 'https://www.songshanculturalpark.org/images/' + \
                    d['ID'] + '/' + d['CoverImage']
                duration = d['PublishDate'].split('~')
                startDate = duration[0].strip().replace('/', '.')
                endDate = duration[-1].strip().replace('/', '.')

                if date.fromisoformat(startDate.replace('.', '-')) < date_A:
                    if date.fromisoformat(endDate.replace('.', '-')) > date_A:
                        pass
                    else:
                        return data

                href = url + '?' + d['ID']
                description = d['SubTitle'].strip()
                description = "".join(description.split())[:50]

                data.append(
                    {'title': title,
                     'image': image,
                     'startDate': startDate,
                     'endDate': endDate,
                     'description': description,
                     'href': href,
                     'type': '展覽活動',
                     'location': '松山文創園區'}
                )
                print(f'爬取頁面「{title}」成功！')
            except:
                pass
        page += 1
    return data


def get_songshan_activity(url, kind, type):
    # 判斷爬取日期
    date_A = datetime.date.today() - datetime.timedelta(days=730)

    data = []
    page = 1
    while True:
        print(f"正在爬取第 {page} 頁")
        my_params = {'kind': kind, 'type': type, 'p': page, 'q': 'get'}
        resp = requests.get(url, params=my_params)
        divs = json.loads(resp.text)['items']  # list 物件
        if not divs:  # divs 為空
            break

        # 整理 json 格式
        for d in divs:
            try:
                title = d['Title'].strip()
                image = 'https://www.songshanculturalpark.org/images/' + \
                    d['ID'] + '/' + d['CoverImageFileName']
                startDate = d['ActivityBeginDate'].strip().replace('/', '.')
                endDate = d['ActivityEndDate'].strip().replace('/', '.')
                if date_A > date.fromisoformat(startDate.replace('.', '-')):
                    return data

                href = url + '?' + d['ID']
                description = d['SubTitle'].strip()
                description = "".join(description.split())[:50]

                data.append(
                    {'title': title,
                     'image': image,
                     'startDate': startDate,
                     'endDate': endDate,
                     'description': description,
                     'href': href,
                     'type': '論壇講座',
                     'location': '松山文創園區'
                     })
                print(f'爬取頁面「{title}」成功！')
            except:
                pass
        page += 1
    return data


def main():
    print('「松山文創園區」爬取開始！')

    songshan = []
    url_1 = 'https://www.songshanculturalpark.org/ExhibitionList.aspx'
    url_2 = 'https://www.songshanculturalpark.org/ActivityList.aspx'
    # 最新活動
    print('正在爬取「最新活動」')
    print('正在爬取「展覽表演」的類別')
    songshan.extend(get_songshan_exhibition(url_1, 0, 1))  # 展覽表演
    print('正在爬取「講座課程」的類別')
    songshan.extend(get_songshan_activity(url_2, 1, 1))  # 講座課程
    # songshan.extend(get_songshan_activity(url_2, 2, 1))  # 其他活動

    # 歷史回顧
    print('正在爬取「歷史回顧」')
    print('正在爬取「展覽表演」的類別')
    songshan.extend(get_songshan_exhibition(url_1, 0, 3))  # 展覽表演
    print('正在爬取「講座課程」的類別')
    songshan.extend(get_songshan_activity(url_2, 1, 3))  # 講座課程
    # songshan.extend(get_songshan_activity(url_2, 2, 3))  # 其他活動

    with open('songshan.json', mode='w', encoding='utf-8') as f:
        json.dump(songshan, f, indent=4, sort_keys=False, ensure_ascii=False)

    print('「松山文創園區」爬取完成！')


if __name__ == '__main__':
    main()

'''
'https://www.songshanculturalpark.org/ExhibitionList.aspx?kind=0&type=1&p=1&q=get'
'https://www.songshanculturalpark.org/ExhibitionList.aspx?kind=0&type=3&p=1&q=get'
'https://www.songshanculturalpark.org/ActivityList.aspx?kind=1&type=1&p=1&q=get'
'https://www.songshanculturalpark.org/ActivityList.aspx?kind=1&type=3&p=1&q=get'
'''
