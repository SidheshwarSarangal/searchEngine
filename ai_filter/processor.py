import json
import re
import ollama
from urllib.parse import urlparse

def classify_blog_entry(entry, model="gemma3:1b"):
    full_content = (entry.get("content") or "").strip()
    title = (entry.get("title") or "").strip()
    url = entry.get("url", "").strip()
    domain = urlparse(url).netloc

    trimmed_content = full_content[:1500] + "\n...\n" + full_content[-1500:]

    # Quick heuristic blocklist — extend this as needed
    known_irrelevant_domains = [
        "www.supermarketnews.com",
        "www.nytimes.com",
        "www.cnn.com",
        "www.forbes.com",
        "www.businessinsider.com",
        "www.reuters.com",
        "www.bbc.com"
    ]

    # Step 1: Domain check
    if domain in known_irrelevant_domains:
        return {
            "title": title or "Untitled",
            "author": entry.get("author", ""),
            "date": entry.get("date", ""),
            "url": url,
            "relevant": False,
            "reason": f"Domain '{domain}' is a known news/corporate site.",
            "summary": ""
        }

    # Step 2: Title generation if missing
    if not title:
        try:
            title_prompt = (
                "Generate a short, meaningful blog title (max 6 words):\n\n"
                f"{trimmed_content}"
            )
            title_response = ollama.chat(model=model, messages=[{"role": "user", "content": title_prompt}])
            title = title_response["message"]["content"].strip()
        except:
            title = "Untitled"

    # Step 3: AI-based relevance & summary
    prompt = (
        "You're a filter deciding whether this is a personal blog or opinion article.\n"
        "Reply ONLY with valid JSON in this format:\n"
        "{\n"
        "  \"relevant\": true or false,\n"
        "  \"reason\": \"short reason\",\n"
        "  \"summary\": \"2-line summary\"\n"
        "}\n\n"
        "Mark relevant = true ONLY IF:\n"
        "- It’s a personal blog, opinion piece, or story.\n"
        "- Uses first-person (I, we) or second-person (you).\n"
        "- NOT news/media/corporate site.\n"
        "- Must contain meaningful content (not just headings/listings).\n\n"
        f"Title: {title}\n\n"
        f"Content:\n{trimmed_content}"
    )

    try:
        ai_response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        raw_output = ai_response["message"]["content"].strip()

        if raw_output.startswith("```json"):
            raw_output = raw_output[7:].strip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].strip()

        raw_output = re.sub(r'[\x00-\x1F]+', ' ', raw_output)
        parsed = json.loads(raw_output)

    except Exception as e:
        parsed = {
            "relevant": False,
            "reason": f"Parsing failed: {str(e)}. Raw: {raw_output[:80] if 'raw_output' in locals() else 'No output'}",
            "summary": ""
        }

    return {
        "title": title,
        "author": entry.get("author", ""),
        "date": entry.get("date", ""),
        "url": url,
        "relevant": parsed.get("relevant", False),
        "reason": parsed.get("reason", "N/A"),
        "summary": parsed.get("summary", "")
    }
