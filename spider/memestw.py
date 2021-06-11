import requests
from bs4 import BeautifulSoup
import json


def get_memestw(url, contest):
    data = []
    page, img_ct = 1, 0
    while True:
        print(f"正在爬取第 {page} 頁")
        my_params = {'contest': contest, 'sort': 'hot', 'page': page}
        resp = requests.get(url, my_params)
        soup = BeautifulSoup(resp.text, 'html.parser')

        divs = soup.find_all('div', 'mb-3 border-bottom pb-3')
        if not divs:  # divs 為空
            break
        for d in divs:
            data.append(d.find('img')['data-src'])
            img_ct += 1
            if img_ct >= 200:
                print(f"爬取該類別的熱門前 {img_ct} 張成功！")
                return data
        page += 1


def main():
    print('「梗圖倉庫」爬取開始！')

    memestw = []
    url = 'https://memes.tw/wtf'
    contests = [795, 29, 41, 8]  # 類別：我自己做的、日常生活、武漢肺炎系列、政治吐槽
    for contest in contests:
        # 判斷類型
        if contest == 795:
            type = '我自己做的'
        elif contest == 29:
            type = '日常生活'
        elif contest == 41:
            type = '武漢肺炎系列'
        elif contest == 8:
            type = '政治吐槽'
        print(f"正在爬取「{type}」的類別")
        memestw.extend(get_memestw(url, contest))

    with open('memestw.json', mode='w', encoding='utf-8') as f:
        json.dump(memestw, f, indent=4, sort_keys=False, ensure_ascii=False)
        # ensure_ascii=False：如果檔案有包含非 ASCII 編碼字元（如所有的中文字，在此是以 utf-8 編碼），仍照常寫入檔案
        # 若 ensure_ascii=True，中文字會變成 \uxxxx 的格式

    print('「梗圖倉庫」爬取完成！')


if __name__ == '__main__':
    main()
