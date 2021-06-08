import json

with open('huashan_new_events.json', mode='r', encoding='utf-8') as f:
    data = json.load(f)  # 讀取檔案

for d in data:
    print(d['beginDate'])
    print(d['endDate'])
    break
