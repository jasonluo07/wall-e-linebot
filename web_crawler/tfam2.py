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
print(html_text)
