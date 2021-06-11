import json

with open('./spider/memestw.json', mode='r', encoding='utf-8') as file:
    memestw = json.load(file)

print(type(memestw))
