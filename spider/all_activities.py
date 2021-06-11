import json

files = ['huashan.json', 'songshan.json', 'tfam.json', 'cksmh.json']

all_activities = []
for file in files:
    with open(file, mode='r', encoding='utf-8') as f:
        all_activities.extend(json.load(f))
print(f'共有 {len(all_activities)} 筆活動')

# 排序方式：活動開始日期由大到小排序
all_activities = sorted(
    all_activities, key=lambda x: x['startDate'], reverse=True)

with open('all_activities.json', mode='w', encoding='utf-8') as f:
    json.dump(all_activities, f, indent=4,
              sort_keys=False, ensure_ascii=False)
