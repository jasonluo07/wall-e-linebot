import requests
from bs4 import BeautifulSoup
import json


def get_events(url, kind, type, file_name):
    events = []
    page = 1
    while True:
        my_params = {'kind': kind, 'type': type, 'p': page, 'q': 'get'}
        resp = requests.get(url, params=my_params)
        current_events = json.loads(resp.text)['items']  # list 物件

        # 整理 json 格式
        for event in current_events:
            image = 'https://www.songshanculturalpark.org/images/' + \
                event['ID'] + '/' + event['CoverImage']
            title = event['Title'].strip()
            date = event['PublishDate'].split('~')
            beginDate = date[0].strip().replace('/', '.')
            endDate = date[-1].strip().replace('/', '.')

            temp_resp = requests.get(url, params={'kind': kind})
            temp_soup = BeautifulSoup(temp_resp.text, 'html.parser')
            temp_type = temp_soup.find('div', 'exhibition title').text
            href = url + '?' + event['ID']
            description = event['SubTitle'].strip().replace(
                '\n', ' ').replace('\r', ' ').replace('  ', ' ')[:40]

            events.append({'image': image,
                           'title': title,
                           'beginDate': beginDate,
                           'endDate': endDate,
                           'description': description,
                           'href': href,
                           'type': temp_type,
                           'location': '松菸',
                           })
        if not current_events:  # current_events 為空
            break
        page += 1

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=4,
                  sort_keys=False, ensure_ascii=False)


url = 'https://www.songshanculturalpark.org/ExhibitionList.aspx'
get_events(url, 0, 1, 'songshan.json')

'''
get_events(url, 0, 3, '松菸_展覽表演_歷史回顧.json')

url = 'https://www.songshanculturalpark.org/ActivityList.aspx'
get_events(url, 1, 1, '松菸_講座課程_最新活動.json')
get_events(url, 1, 3, '松菸_講座課程_歷史回顧.json')
get_events(url, 2, 1, '松菸_其他活動_最新活動.json')
get_events(url, 2, 3, '松菸_其他活動_歷史回顧.json')
'''
