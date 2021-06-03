import json

with open('test.json', mode='r') as f:
    data = json.load(f)
print(type(data[0]))
