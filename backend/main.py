from fastapi import FastAPI, Query
from es_config import es, INDEX_NAME

app = FastAPI()

@app.get("/search")
def search_blogs(q: str = Query(..., description="Search query")):
    body = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["title^3", "author^2", "content"]
            }
        }
    }

    res = es.search(index=INDEX_NAME, body=body, size=10)
    hits = res["hits"]["hits"]

    return {
        "results": [
            {
                "title": hit["_source"]["title"],
                "author": hit["_source"]["author"],
                "summary": hit["_source"]["summary"],
                "url": hit["_source"]["url"],
                "score": hit["_score"]
            }
            for hit in hits
        ]
    }
