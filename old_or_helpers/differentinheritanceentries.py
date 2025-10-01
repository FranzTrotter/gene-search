import json

# Load the JSON files
with open('updated_records.json') as f1, open('updated_records6.json') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

# Build a mapping from id to inheritance for quick lookup
inheritance_map1 = {item['_id']: item['inheritance'] for item in data1}
inheritance_map2 = {item['_id']: item['inheritance'] for item in data2}

# Find IDs where inheritance values differ
different_ids = [
    id_ for id_ in inheritance_map1
    if inheritance_map1.get(id_) != inheritance_map2.get(id_)
]

print(different_ids)