import requests
from bs4 import BeautifulSoup
import json

from function import *

# 松菸_展覽表演_最新活動
url = 'https://www.songshanculturalpark.org/ExhibitionList.aspx'
get_events(url, 0, 1, '松菸_展覽表演_最新活動.json')

# 松菸_展覽表演_歷史回顧
get_events(url, 0, 3, '松菸_展覽表演_歷史回顧.json')

# 松菸_講座課程_最新活動
url = 'https://www.songshanculturalpark.org/ActivityList.aspx'
get_events(url, 1, 1, '松菸_講座課程_最新活動.json')

# 松菸_講座課程_歷史回顧
get_events(url, 1, 3, '松菸_講座課程_歷史回顧.json')

# 松菸_其他活動_最新活動
url = 'https://www.songshanculturalpark.org/ActivityList.aspx'
get_events(url, 2, 1, '松菸_其他活動_最新活動.json')

# 松菸_其他活動_歷史回顧
get_events(url, 2, 3, '松菸_其他活動_歷史回顧.json')
