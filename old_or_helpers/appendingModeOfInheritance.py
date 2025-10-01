import json
import re

# Load JSON data
with open("records.json", "r", encoding="utf-8") as f:
    summary_data = json.load(f)

with open("datacopy.json", "r", encoding="utf-8") as f:
    full_text_data = json.load(f)

# Inheritance keywords
inheritance_patterns = {
    "autosomal recessive": [
        r"autosomal recessive (inheritance|manner|pattern|disorder)",
        r"inherited in an autosomal recessive manner",
        r"autosomal recessive"
    ],
    "autosomal dominant": [
        r"autosomal dominant (inheritance|manner|pattern|disorder)",
        r"inherited in an autosomal dominant manner",
        r"autosomal dominant"
    ],
    "autosomal codominant": [
        r"autosomal codominant (inheritance|manner|pattern|disorder)",
        r"inherited in an autosomal codominant manner",
        r"autosomal codominant"
    ],
    "x-linked": [
        r"\bx[- ]linked\b",
        r"\bX[- ]linked\b",
        r"inherited in an x[- ]linked manner"
    ],
     "y-linked": [
        r"\by[- ]linked\b",
        r"\by[- ]linked\b",
        r"inherited in an y[- ]linked manner"
    ],
    "mitochondrial": [
        r"mitochondrial inheritance",
        r"maternal inheritance",
        r"\bin mtDNA\b"
        r"inherited from the mother"
    ]
}

def detect_inheritance(text):
    text = text.lower()
    found_labels = []
    for label, patterns in inheritance_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found_labels.append(label)
                break
    return found_labels

# Update inheritance field
for entry in summary_data:
    entry_id = entry["_id"]
    full_entry = full_text_data.get(entry_id, {})
    combined_text = ""

    # Prioritize specific sections, but include all text if needed
    for section in ["Genetic Counseling", "Summary"]:
        section_data = full_entry.get(section)
        if section_data:
            combined_text += " " + section_data.get("text", "")

    found_labels = detect_inheritance(combined_text)

    entry["inheritance"] = sorted(set(found_labels))

# Save updated output
with open("updated_records.json", "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)
