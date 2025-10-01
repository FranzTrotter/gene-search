import json

# Load records
with open('records_without_metadata.json', 'r') as f:
    records = json.load(f)
list=["hi","was"]

# Add metadata to each
for record in records:
    record['inheritance'] = "unknown"

# Save back to file
with open('records.json', 'w') as f:
    json.dump(records, f, indent=2)
