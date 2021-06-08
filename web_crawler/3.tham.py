from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import json
import time

my_options = Options()
# my_options.add_argument('--headless')  # 不開啟實體瀏覽器執行
my_options.add_argument('--start-maximized')  # 視窗最大化

url = 'https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw'  # 當期展覽
driver = webdriver.Chrome(options=my_options)
driver.get(url)
html_text = driver.page_source  # 取得網頁原始碼
soup_tfam = BeautifulSoup(html_text, 'html.parser')

events = []
divs = soup_tfam.find_all('div', 'row Exhibition_list')
for i in range(len(divs)):
    image = divs[i].find('img')['src']
    title = divs[i].find('h3').text
    print(title)
    date = divs[i].find('p', 'date-middle').text.split('-')
    beginDate = date[0].strip().replace('/', '.')
    endDate = date[-1].strip().replace('/', '.')
    info = driver.find_element_by_xpath(
        f'//*[@id="ExList"]/div[{i+1}]/div[2]/h3/a')
    info.click()
    time.sleep(1)

    windows = driver.window_handles
    if len(windows) != 1:
        driver.switch_to.window(windows[-1])
        href = driver.current_url
        driver.close()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
    else:
        href = driver.current_url
        driver.back()

    events.append({
        'image': image,
        'title': title,
        'beginDate': beginDate,
        'endDate': endDate,
        'description': 'manual update',
        'href': href,
        'type': '展覽活動',
        'location': '臺北市立美術館'
    })

with open('tfam_new_events.json', mode='w', encoding='utf-8') as f:
    json.dump(events, f, indent=4, sort_keys=False, ensure_ascii=False)
    # ensure_ascii=False：如果檔案有包含非 ASCII 編碼字元（如所有的中文字，在此是以 utf-8 編碼），仍照常寫入檔案
    # 若 ensure_ascii=True，中文字會變成 \uxxxx 的格式
