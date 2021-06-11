import json
import datetime
from datetime import date

with open('all_activities.json', mode='r', encoding='utf-8') as f:
    all_activities = json.load(f)

target_date = datetime.date.today()

# activitiesA
activitiesA = []
for i in range(len(all_activities)):
    type = all_activities[i]['type']
    start_date = date.fromisoformat(
        all_activities[i]['startDate'].replace('.', '-'))
    end_date = date.fromisoformat(
        all_activities[i]['endDate'].replace('.', '-'))
    boolean1 = '展覽活動' in type
    if (target_date <= start_date) & (target_date <= end_date):
        boolean2 = True
    elif start_date <= target_date <= end_date:
        boolean2 = True
    else:
        boolean2 = False
    if boolean1 & boolean2:
        activitiesA.append(all_activities[i])

with open('activitiesA.json', mode='w', encoding='utf-8') as f:
    json.dump(activitiesA, f, indent=4,
              sort_keys=False, ensure_ascii=False)

# activitiesB
activitiesB = []
for i in range(len(all_activities)):
    type = all_activities[i]['type']
    start_date = date.fromisoformat(
        all_activities[i]['startDate'].replace('.', '-'))
    end_date = date.fromisoformat(
        all_activities[i]['endDate'].replace('.', '-'))
    boolean1 = '表演活動' in type
    if (target_date <= start_date) & (target_date <= end_date):
        boolean2 = True
    elif start_date <= target_date <= end_date:
        boolean2 = True
    else:
        boolean2 = False
    if boolean1 & boolean2:
        activitiesB.append(all_activities[i])

with open('activitiesB.json', mode='w', encoding='utf-8') as f:
    json.dump(activitiesB, f, indent=4,
              sort_keys=False, ensure_ascii=False)

# activitiesC
activitiesC = []
for i in range(len(all_activities)):
    type = all_activities[i]['type']
    start_date = date.fromisoformat(
        all_activities[i]['startDate'].replace('.', '-'))
    end_date = date.fromisoformat(
        all_activities[i]['endDate'].replace('.', '-'))
    boolean1 = '品牌活動' in type
    if (target_date <= start_date) & (target_date <= end_date):
        boolean2 = True
    elif start_date <= target_date <= end_date:
        boolean2 = True
    else:
        boolean2 = False
    if boolean1 & boolean2:
        activitiesC.append(all_activities[i])

with open('activitiesC.json', mode='w', encoding='utf-8') as f:
    json.dump(activitiesC, f, indent=4,
              sort_keys=False, ensure_ascii=False)

# activitiesD
activitiesD = []
for i in range(len(all_activities)):
    type = all_activities[i]['type']
    start_date = date.fromisoformat(
        all_activities[i]['startDate'].replace('.', '-'))
    end_date = date.fromisoformat(
        all_activities[i]['endDate'].replace('.', '-'))
    boolean1 = '論壇講座' in type
    if (target_date <= start_date) & (target_date <= end_date):
        boolean2 = True
    elif start_date <= target_date <= end_date:
        boolean2 = True
    else:
        boolean2 = False
    if boolean1 & boolean2:
        activitiesD.append(all_activities[i])

with open('activitiesD.json', mode='w', encoding='utf-8') as f:
    json.dump(activitiesD, f, indent=4,
              sort_keys=False, ensure_ascii=False)
