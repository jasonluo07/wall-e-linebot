from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import json
import time
import pyautogui

my_options = Options()
# my_options.add_argument('--headless')  # 不開啟實體瀏覽器執行
my_options.add_argument('--start-maximized')  # 視窗最大化

url = 'https://www.tfam.museum/Exhibition/Exhibition_Special.aspx?ddlLang=zh-tw&id=686&allObj=%7B%22JJMethod%22%3A%22GetEx%22%2C%22Type%22%3A%221%22%7D'
# url2 = 'https://www.tfam.museum/Exhibition/Exhibition_page.aspx?ddlLang=zh-tw&id=685&allObj=%7B%22JJMethod%22%3A%22GetEx%22%2C%22Type%22%3A%221%22%7D'
# url3 = 'https://www.tfam.museum/Exhibition/Exhibition_page.aspx?ddlLang=zh-tw&id=681&allObj=%7B%22JJMethod%22%3A%22GetEx%22%2C%22Type%22%3A%221%22%7D'
# urls = [url1, url2, url3]

driver = webdriver.Chrome(options=my_options)
driver.get(url)
time.sleep(2)

actions = webdriver.ActionChains(driver)
time.sleep(1)
driver.execute_script('window.scrollTo(0, 500)')  # 滾動頁面至 y 軸 500 單位
time.sleep(1)
actions.move_by_offset(500, 500).double_click(
).double_click()  # 移動滑鼠至坐標(500, 500)，雙擊左鍵兩次
actions.key_down(Keys.CONTROL).send_keys('c').key_up(
    Keys.CONTROL).perform()  # 使用鍵盤，ctrl + c（複製）
actions.key_down(Keys.CONTROL).send_keys('v').key_up(
    Keys.CONTROL).perform()  # 使用鍵盤，ctrl + v（貼上）
