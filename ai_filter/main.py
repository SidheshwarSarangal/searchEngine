import json
import yaml
from processor import classify_blog_entry

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

with open(config["input_path"], "r", encoding="utf-8") as f:
    data = json.load(f)

processed = []
for entry in data:
    result = classify_blog_entry(entry, model=config["model"])
    processed.append(result)  # ✅ Use only cleaned data

# Save results
with open(config["output_path"], "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print("Processing complete. Output saved.")
