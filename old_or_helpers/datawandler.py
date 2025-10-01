#takes the entire dataset for GeneReviews and organizes in a 'only summary way'
import json

# Load your original JSON data
with open('data_copy_20250401.json', 'r') as f:
    data = json.load(f)

# Convert to desired format
records = []
for name, sections in data.items():
    summary_text = sections.get('Summary', {}).get('text', '')
    records.append({'_id': name, 'chunk_text': summary_text, "mortality": "unknown", "inheritance": "unknown", "penetrance": "unknown"})

# Save the new structure to a new JSON file
with open('records.json', 'w') as f:
    json.dump(records, f, indent=2)
