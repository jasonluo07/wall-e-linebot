import requests
from bs4 import BeautifulSoup
import json


def get_events(url, file_name):
    events = []  # 儲存取得的活動資料
    page = 1
    while True:
        my_params = {'index': page}
        resp = requests.get(url, params=my_params)
        soup_current_page = BeautifulSoup(resp.text, 'html.parser')

        divs = soup_current_page.find('div', 'event-list').find_all('li')
        if not divs:
            break
        for d in divs:
            event_name = d.find('div', 'card-text-name').text.strip()
            event_image = d.find(
                'div', 'card-img wide')['style'].split('url')[1].replace('(\'', '').replace('\')', '')
            event_date = d.find('div', 'event-date').text.strip()
            try:  # 活動時間，有些可能沒有活動時間
                event_time = d.find(
                    'div', {'class': 'event-time'}).text.strip()
            except:
                event_time = ''
            event_type = d.find('div', 'event-list-type').text.strip()
            event_link = 'https://www.huashan1914.com/' + d.find('a')['href']

            events.append({
                'event_name': event_name,
                'event_image': event_image,
                'event_date': event_date,
                'event_type': event_type,
                'event_link': event_link
            })
        page += 1

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=4, sort_keys=False, ensure_ascii=False)