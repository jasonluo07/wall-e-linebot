import requests
from bs4 import BeautifulSoup
import json


def get_huashan_events(url):
    events = []
    page = 1
    while True:
        my_params = {'index': page}
        resp = requests.get(url, params=my_params)
        soup_current_page = BeautifulSoup(resp.text, 'html.parser')

        divs = soup_current_page.find('div', 'event-list').find_all('li')
        if not divs:  # divs 為空
            break
        for d in divs:
            title = d.find('div', 'card-text-name').text.strip()
            image = d.find(
                'div', 'card-img wide')['style'].split('url')[1].replace('(\'', '').replace('\')', '')
            date = d.find('div', 'event-date').text.strip()
            beginDate = date.split('-')[0].strip()
            endDate = date.split('-')[-1].strip()
            type = d.find('div', 'event-list-type').text.strip().split()
            href = 'https://www.huashan1914.com/' + d.find('a')['href']

            # 進入活動頁面，爬活動描述
            resp = requests.get(href)
            soup_event = BeautifulSoup(resp.text, 'html.parser')

            description = soup_event.find(
                'div', 'card-text-info').text.strip().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')[:40]
            events.append({
                'title': title,
                'image': image,
                'beginDate': beginDate,
                'endDate': endDate,
                'type': type,
                'href': href,
                'description': description
            })
        page += 1
    return events


events = []
# 爬取新的活動
events.extend(get_huashan_events(
    'https://www.huashan1914.com/w/huashan1914/exhibition'))
'''
# 爬取舊的活動
events.extend(get_huashan_events(
    'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-1'))
'''

with open('huashan.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, indent=4, sort_keys=False, ensure_ascii=False)
    # ensure_ascii=False：如果檔案有包含非 ASCII 編碼字元（如所有的中文字，在此是以 utf-8 編碼），仍照常寫入檔案
    # 若 ensure_ascii=True，中文字會變成 \uxxxx 的格式
