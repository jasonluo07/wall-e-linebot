import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from datetime import date


import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date


def get_huashan(url):
    date_A = datetime.date.today() - datetime.timedelta(days=1095)  # 爬取近三年資料

    events = []
    index = 1

    while True:
        print(f"正在爬取第 {index} 頁")
        my_params = {'index': index}
        resp = requests.get(url, params=my_params)
        soup_huashan = BeautifulSoup(resp.text, 'html.parser')

        divs = soup_huashan.find(
            'ul', {'id': 'event-ul'}).find_all('li', 'item-static')
        if not divs:  # divs 為空
            break

        for d in divs:
            try:
                title = d.find('div', 'card-text-name').text.strip()
                image = d.find('div', 'card-img-content')['style'].split(
                    'url')[-1].replace("(\'", '').replace("\')", '')

                duration = d.find('div', 'event-date').text.strip().split('-')
                startDate = duration[0].strip()
                endDate = duration[-1].strip()
                if startDate == endDate:
                    pass
                elif len(startDate.split('.')) == len(endDate.split('.')):
                    pass
                elif endDate.split('.')[0] >= startDate.split('.')[1]:
                    endDate = startDate.split('.')[0] + '.' + endDate
                else:
                    print('ERROR!')

                if date.fromisoformat(startDate.replace('.', '-')) < date_A:
                    if date.fromisoformat(endDate.replace('.', '-')) > date_A:
                        pass
                    else:
                        return events

                href = 'https://www.huashan1914.com' + d.find('a')['href']
                # 進入活動頁面，爬取活動描述
                resp = requests.get(href)
                soup_event = BeautifulSoup(resp.text, 'html.parser')
                type = '&&'.join([i.text for i in soup_event.find(
                    'div', {'id': 'divChips'}).find_all('span', 'chip-name')])
                type.replace('展演活動', '展覽活動').replace('表演藝術', '表演活動')

                description = soup_event.find('div', 'card-text-info').text
                description = "".join(description.split())[:50]

                this_event = {
                    'title': title,
                    'image': image,
                    'startDate': startDate,
                    'endDate': endDate,
                    'description': description,
                    'href': href,
                    'type': type,
                    'location': '華山文創意園區'
                }

                if this_event in events:
                    break

                events.append(this_event)
                print(f'爬取頁面「{title}」成功！')
            except:
                pass
        index += 1
    return events


def main():
    print('「華山文創園區」爬取開始！')

    huashan = []
    print('正在爬取「展演活動」的類別')
    huashan.extend(get_huashan(
        'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17111317255246856'))
    print('正在爬取「論壇講座」的類別')
    huashan.extend(get_huashan(
        'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410124681532'))
    print('正在爬取「品牌活動」的類別')
    huashan.extend(get_huashan(
        'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410122600181'))
    print('正在爬取「表演藝術」的類別')
    huashan.extend(get_huashan(
        'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-2'))

    # 排序方式：活動開始日期由大到小排序
    huashan = sorted(huashan, key=lambda x: x['startDate'], reverse=True)

    with open('huashan.json', mode='w', encoding='utf-8') as f:
        json.dump(huashan, f, indent=4, sort_keys=False, ensure_ascii=False)
        # ensure_ascii=False：如果檔案有包含非 ASCII 編碼字元（如所有的中文字，在此是以 utf-8 編碼），仍照常寫入檔案
        # 若 ensure_ascii=True，中文字會變成 \uxxxx 的格式

    print('「華山文創園區」爬取完成！')


if __name__ == '__main__':
    main()
