from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

my_options = Options()
# my_options.add_argument('--headless')  # 不開啟實體瀏覽器執行
my_options.add_argument('--start-maximized')  # 視窗最大化
my_options.add_argument('--incognito')  # 使用無痕模式

driver = webdriver.Chrome(options=my_options)
url = 'https://kktix.com/?locale=zh-TW'
driver.get(url)

explore_btn = driver.find_element_by_xpath('//*[@id="navbar"]/ul[1]/li[2]')
explore_btn.click()  # 選擇「探索活動」
type_choice = driver.find_element_by_xpath(
    '//*[@id="new_search_form"]/div/div/div[2]/div[2]/ul/li[11]')
type_choice.click()  # 選擇「藝文活動」


while True:
    info = driver.find_elements_by_class_name('fa-angle-right')
    for i in range(len(info)):
        info = driver.find_elements_by_class_name('fa-angle-right')
        print(info)
        info[i].click()
        time.sleep(1)

        title = driver.find_element_by_class_name('header-title')
        timezone = driver.find_elements_by_class_name('timezoneSuffix')
        beginDate = timezone[0].text
        endDate = timezone[1].text
        driver.back()  # 上一頁
        time.sleep(2)  # 避免爬太快

    next_page = driver.find_elements_by_xpath(
        '/html/body/div[3]/div[2]/section[1]/div/div[2]/ul/li')
    try:
        if next_page[-1].text != '›':  # 最後一頁時，不能翻頁
            print(f"共 {next_page[-1].text} 頁")
            break
        next_page[-1].click()
    except IndexError:
        break
