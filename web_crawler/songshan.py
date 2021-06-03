import requests
from bs4 import BeautifulSoup
import json


def get_events(url, kind, type, file_name):
    events = []
    page = 1
    while True:
        my_params = {'kind': kind, 'type': type, 'p': page, 'q': 'get'}
        resp = requests.get(url, params=my_params)
        current_events = json.loads(resp.text)['items']
        events.extend(current_events)
        if not current_events:
            break
        page += 1

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=4, sort_keys=False, ensure_ascii=False)
