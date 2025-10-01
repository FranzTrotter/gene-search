import json
import re

# File paths (change these as needed)
file1_path = 'records.json'   # List of dicts
file2_path = 'datacopy.json'        # Dict of dicts

# Load JSON files
with open(file1_path, 'r', encoding='utf-8') as f:
    data1 = json.load(f)

with open(file2_path, 'r', encoding='utf-8') as f:
    data2 = json.load(f)

def extract_text(gc_section):
    # Extract the 'text' field from the Genetic Counseling section.
    if isinstance(gc_section, dict):
        return gc_section.get("text", "")
    return ""

# Define inheritance modes to look for
modes = {
    'autosomal recessive': re.compile(r'\bautosomal recessive\b', re.IGNORECASE),
    'autosomal dominant': re.compile(r'\bautosomal dominant\b', re.IGNORECASE),
    'autosomal codominant': re.compile(r'\bautosomal codominant manner\b', re.IGNORECASE),
    'x-linked': re.compile(r'\bx[- ]linked\b', re.IGNORECASE),
    'mitochondrial': re.compile(r'\b(mitochondrial(\s*\(maternal\))?|maternal(\s*\(mitochondrial\))?) inheritance\b', re.IGNORECASE),
    'multifactorial': re.compile(r'\bmultifactorial\b', re.IGNORECASE)
}

# Convert data1 to a dict for quick access by _id
data1_dict = {_['_id']: _ for _ in data1}

# Keep track of entries to delete from data2
keys_to_delete = []

for key, value in data2.items():
    genetic_counseling_text = extract_text(value.get("Genetic Counseling", {}))

    # Check for each mode
    for mode, pattern in modes.items():
        if pattern.search(genetic_counseling_text):
            if key in data1_dict:
                data1_dict[key]['inheritance'] = mode
            keys_to_delete.append(key)
            break  # Stop checking after first match

# Apply deletions
for key in keys_to_delete:
    del data2[key]

# Convert back to list for saving data1
updated_data1 = list(data1_dict.values())

# Save updated files
with open('updated_records.json', 'w', encoding='utf-8') as f:
    json.dump(updated_data1, f, ensure_ascii=False, indent=2)

with open('filtered_datacopy.json', 'w', encoding='utf-8') as f:
    json.dump(data2, f, ensure_ascii=False, indent=2)
