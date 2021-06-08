import requests
from bs4 import BeautifulSoup
import time
import json

# url = 'https://www.huashan1914.com/w/huashan1914/exhibition'
url = 'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-2'
events = []
page = 1

while True:
    if page == 3:
        break
    print(f'current_page: {page}')
    my_params = {'index': page}
    resp = requests.get(url, params=my_params)
    soup_current_page = BeautifulSoup(resp.text, 'html.parser')

    divs = soup_current_page.find('div', 'event-list').find_all('li')
    if not divs:  # divs 為空
        break
    for d in divs:
        image = d.find(
            'div', 'card-img wide')['style'].split('url')[1].replace('(\'', '').replace('\')', '')
        title = d.find('div', 'card-text-name').text.strip()
        date = d.find('div', 'event-date').text.strip()
        beginDate = date.split('-')[0].strip()
        endDate = date.split('-')[-1].strip()
        type = d.find(
            'div', 'event-list-type').text.strip().replace('\n', '&&')
        href = 'https://www.huashan1914.com/' + d.find('a')['href']

        # 進入活動頁面，爬取活動描述
        resp = requests.get(href)
        soup_event = BeautifulSoup(resp.text, 'html.parser')
        description = soup_event.find('div', 'card-text-info').text.strip().replace(
            '\n', ' ').replace('\r', ' ').replace('  ', ' ')[:40]

        events.append({
            'image': image,
            'title': title,
            'beginDate': beginDate,
            'endDate': endDate,
            'description': description,
            'href': href,
            'type': type,
            'location': '華山'
        })
    page += 1

with open('huashan_brand.json', mode='w', encoding='utf-8') as f:
    json.dump(events, f, indent=4, sort_keys=False, ensure_ascii=False)
    # ensure_ascii=False：如果檔案有包含非 ASCII 編碼字元（如所有的中文字，在此是以 utf-8 編碼），仍照常寫入檔案
    # 若 ensure_ascii=True，中文字會變成 \uxxxx 的格式