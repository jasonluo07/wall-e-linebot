import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from datetime import date


def get_songshan(url, kind, type):
    # 判斷爬取日期
    today = datetime.date.today()
    date_A = today - datetime.timedelta(days=730)

    data = []
    page = 1
    while True:
        print(f"正在爬取第 {page} 頁")
        my_params = {'kind': kind, 'type': type, 'p': page, 'q': 'get'}
        resp = requests.get(url, params=my_params)
        divs = json.loads(resp.text)['items']  # list 物件

        # 整理 json 格式
        for d in divs:
            try:
                image = 'https://www.songshanculturalpark.org/images/' + \
                    d['ID'] + '/' + d['CoverImage']
                title = d['Title'].strip()
                print(title)
                duration = d['PublishDate'].split('~')
                startDate = duration[0].strip().replace('/', '.')
                endDate = duration[-1].strip().replace('/', '.')
                if date_A > date.fromisoformat(startDate.replace('.', '-')):
                    return data

                re = requests.get(url, params={'kind': kind})
                soup = BeautifulSoup(re.text, 'html.parser')
                type = soup.find('div', 'exhibition title').text
                href = url + '?' + d['ID']
                description = d['SubTitle'].strip().replace(
                    '\n', ' ').replace('\r', ' ').replace('  ', ' ')[:40]

                data.append(
                    {'image': image,
                     'title': title,
                     'startDate': startDate,
                     'endDate': endDate,
                     'description': description,
                     'href': href,
                     'type': type,
                     'location': '松菸'
                     })
            except:
                pass
        if not divs:  # divs 為空
            break
        page += 1
    return data


def main():
    print('「松山文創園區」爬取開始！')

    songshan = []
    url_1 = 'https://www.songshanculturalpark.org/ExhibitionList.aspx'
    url_2 = 'https://www.songshanculturalpark.org/ActivityList.aspx'
    # 最新活動
    print('正在爬取「最新滑動」')
    print('正在爬取「展覽表演」的類別')
    songshan.append(get_songshan(url_1, 0, 1))  # 展覽表演
    print('正在爬取「講座課程」的類別')
    songshan.append(get_songshan(url_2, 1, 1))  # 講座課程
    # songshan.append(get_songshan(url_2, 2, 1))  # 其他活動

    # 歷史回顧
    print('正在爬取「歷史回顧」')
    print('正在爬取「展覽表演」')
    songshan.append(get_songshan(url_1, 0, 3))  # 展覽表演
    print('正在爬取「講座課程」的類別')
    songshan.append(get_songshan(url_2, 1, 3))  # 講座課程
    # songshan.append(get_songshan(url_2, 2, 3))  # 其他活動

    with open('songshan.json', mode='w', encoding='utf-8') as f:
        json.dump(songshan, f, indent=4, sort_keys=False, ensure_ascii=False)


if __name__ == '__main__':
    main()


url = 'https://www.songshanculturalpark.org/ExhibitionList.aspx'
get_songshan(url, 0, 1, 'songshan2.json')

'''
get_events(url, 0, 3, '松菸_展覽表演_歷史回顧.json')

url = 'https://www.songshanculturalpark.org/ActivityList.aspx'
get_events(url, 1, 1, '松菸_講座課程_最新活動.json')
get_events(url, 1, 3, '松菸_講座課程_歷史回顧.json')
get_events(url, 2, 1, '松菸_其他活動_最新活動.json')
get_events(url, 2, 3, '松菸_其他活動_歷史回顧.json')
'''
