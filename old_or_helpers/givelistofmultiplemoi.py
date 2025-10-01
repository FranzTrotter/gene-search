import json

# Load the JSON files
with open('updated_records.json') as f1:
    data = json.load(f1)

list = []

for item in data:
    if len(item["inheritance"]) > 1:
        list.append(item["_id"])
print(list)