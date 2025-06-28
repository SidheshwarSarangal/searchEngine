from pymongo import MongoClient
from es_config import es, INDEX_NAME

# MongoDB connection
MONGO_URI = "mongodb+srv://srchEngn:srchEngn123@cluster0.ut32dlk.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["personal_blogs"]
collection = db["entries"]

# Create index if it doesn’t exist
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)
    print(f"🆕 Created index: {INDEX_NAME}")
else:
    print(f"ℹ️ Index already exists: {INDEX_NAME}")

count = 0
skipped = 0

for entry in collection.find():
    entry.pop("_id", None)
    url = entry.get("url")
    if not url:
        continue

    # ✅ Skip if already indexed in Elasticsearch
    if es.exists(index=INDEX_NAME, id=url):
        skipped += 1
        continue

    es.index(index=INDEX_NAME, id=url, body=entry)
    count += 1

print(f"✅ Indexed: {count} new entries")
print(f"⏭️ Skipped: {skipped} already existing entries")
