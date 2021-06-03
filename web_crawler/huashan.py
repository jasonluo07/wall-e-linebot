import requests
from bs4 import BeautifulSoup
import json

from huashan_func import *


get_events('https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17111317255246856', '華山_展演活動.json')
get_events('https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410123492438', '華山_期間限定店.json')
get_events('https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410124681532', '華山_論壇講座.json')
get_events('https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410130478518', '華山_市集活動.json')
get_events(
    'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-2', '華山_表演藝術.json')
get_events(
    'https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-1', '華山_歷史活動.json')


# 展演活動
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17111317255246856
# 期間限定店
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410123492438
# 論壇講座
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410124681532
# 市集活動
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410130478518
# 品牌活動
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=17090410122600181
# 表演藝術
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-2
# 歷史活動
# https://www.huashan1914.com/w/huashan1914/exhibition?typeId=-1
