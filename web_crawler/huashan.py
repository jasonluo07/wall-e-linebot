import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from datetime import date


def get_huashan(url):
    # 判斷爬取日期
    today = datetime.date.today()
    date_A = today - datetime.timedelta(days=1095)  # 爬取近三年資料

    # 爬取程式
    data = []
    page = 1
    while True:
        print(f"正在爬取第 {page} 頁")
        my_params = {'index': page}
        resp = requests.get(url, params=my_params)
        soup = BeautifulSoup(resp.text, 'html.parser')

        divs = soup.find('div', 'event-list').find_all('li')
        if not divs:  # divs 為空
            break
        for d in divs:
            try:
                title = d.find('div', 'card-text-name').text.strip()
                print(title)
                image = d.find(
                    'div', 'card-img wide')['style'].split('url')[1].replace('(\'', '').replace('\')', '')
                duration = d.find('div', 'event-date').text.strip()
                startDate = duration.split('-')[0].strip()
                endDate = duration.split('-')[-1].strip()
                if date_A > date.fromisoformat(startDate.replace('.', '-')):
                    return data

                href = 'https://www.huashan1914.com/' + d.find('a')['href']
                # 進入活動頁面，爬取活動描述
                resp = requests.get(href)
                soup_event = BeautifulSoup(resp.text, 'html.parser')
                endDate = soup_event.find_all(
                    'div', 'card-date')[1].find('div', 'year').text + '.' + endDate
                type = soup_event.find_all('span', 'chip-name')
                for i in range(len(type)):
                    type[i] = type[i].text.strip()
                    if type[i] == '展演活動':
                        type[i] = '展覽活動'
                    elif type[i] == '表演藝術':
                        type[i] == '表演活動'

                description = soup_event.find('div', 'card-text-info').text.strip().replace(
                    '\n', ' ').replace('\r', ' ').replace('  ', ' ')[:50]

                data.append({
                    'title': title,
                    'image': image,
                    'startDate': startDate,
                    'endDate': endDate,
                    'description': description,
                    'href': href,
                    'type': type,
                    'location': '華山文創意園區'
                })
            except:
                pass
        page += 1
    return data


def main():
    print('「華山文創園區」爬取開始！')

    huashan = []
    print('正在爬取「最新活動」的類別')
    huashan.extend(get_huashan(
        'https://www.huashan1914.com/w/huashan1914/exhibition'))
    print('正在爬取「歷史活動」的類別')
    huashan.extend(get_huashan(
        'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-1'))

    with open('huashan.json', mode='w', encoding='utf-8') as f:
        json.dump(huashan, f, indent=4, sort_keys=False, ensure_ascii=False)
        # ensure_ascii=False：如果檔案有包含非 ASCII 編碼字元（如所有的中文字，在此是以 utf-8 編碼），仍照常寫入檔案
        # 若 ensure_ascii=True，中文字會變成 \uxxxx 的格式

    print('「華山文創園區」爬取完成！')


if __name__ == '__main__':
    main()
