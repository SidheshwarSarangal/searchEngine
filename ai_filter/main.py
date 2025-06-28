import json
import yaml
from processor import classify_blog_url

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load URL list
with open(config["input_path"], "r", encoding="utf-8") as f:
    urls = json.load(f)

processed = []
for i, url in enumerate(urls):
    print(f"🔗 [{i+1}/{len(urls)}] Processing: {url}")
    result = classify_blog_url(url, model=config["model"])
    processed.append(result)

# Save results
with open(config["output_path"], "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print("✅ Processing complete. Output saved to", config["output_path"])
