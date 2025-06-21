from pymongo import MongoClient
from es_config import es, INDEX_NAME

# MongoDB Atlas URI
MONGO_URI = "mongodb+srv://srchEngn:srchEngn123@cluster0.ut32dlk.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["personal_blogs"]
collection = db["entries"]

# Create index if not exists
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

# Push each MongoDB blog to OpenSearch
for entry in collection.find():
    entry.pop("_id", None)  # 🔥 Remove MongoDB's ObjectId field
    es.index(index=INDEX_NAME, id=entry["url"], body=entry)

print("✅ MongoDB -> Elasticsearch indexing complete.")
