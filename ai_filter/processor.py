import json
import re
import ollama
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clean_html_content(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text)

def classify_blog_entry(entry, model="gemma3:1b"):
    raw_html = entry.get("content", "")
    full_content = clean_html_content(raw_html)
    title = (entry.get("title") or "").strip()
    url = entry.get("url", "").strip()
    domain = urlparse(url).netloc

    trimmed_content = full_content[:1500]

    known_irrelevant_domains = [
        "www.supermarketnews.com",
        "www.nytimes.com",
        "www.cnn.com",
        "www.forbes.com",
        "www.businessinsider.com",
        "www.reuters.com",
        "www.bbc.com",
        "hbr.org",
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

    # Step 2: Generate title if missing
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

    # Step 3: AI classification
    prompt = (
        "You're an AI deciding if the following is a personal blog or opinion article.\n"
        "Respond ONLY with this exact JSON format:\n"
        "{\n"
        "  \"relevant\": true or false,\n"
        "  \"reason\": \"short reason\",\n"
        "  \"summary\": \"2-line summary\"\n"
        "}\n\n"
        "Personal blog if:\n"
        "- It is written in first person ('I', 'we') or second person ('you'),\n"
        "- It shares opinions, stories, or personal experiences,\n"
        "- It is NOT from a corporate/news/media source.\n\n"
        f"Title: {title}\n\n"
        f"Content:\n{trimmed_content}"
    )

    relevant = False
    reason = "No response from model"
    summary = ""

    try:
        ai_response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        raw_output = ai_response["message"]["content"].strip()
        print("\n🔍 Raw AI Output:\n", raw_output)

        if raw_output.startswith("```json"):
            raw_output = raw_output[7:].strip()
        elif raw_output.startswith("```"):
            raw_output = raw_output[3:].strip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].strip()

        raw_output = re.sub(r'[\x00-\x1F]+', ' ', raw_output)
        parsed = json.loads(raw_output)

        relevant = parsed.get("relevant", False)
        reason = parsed.get("reason", "").strip() or "AI marked as relevant but gave no reason."
        summary = parsed.get("summary", "").strip()

    except Exception as e:
        reason = f"Parsing failed: {str(e)}. Raw: {raw_output[:80] if 'raw_output' in locals() else 'No output'}"
        summary = ""

    # Step 4: Fallback summary if model gave nothing
    if not summary:
        try:
            summary_prompt = (
                "Summarize the following blog post in exactly 2 informative lines. Avoid general or vague text.\n\n"
                f"{trimmed_content}"
            )
            summary_response = ollama.chat(model=model, messages=[{"role": "user", "content": summary_prompt}])
            summary = summary_response["message"]["content"].strip()
        except:
            summary = "Summary generation failed."

    return {
        "title": title,
        "author": entry.get("author", ""),
        "date": entry.get("date", ""),
        "url": url,
        "relevant": relevant,
        "reason": reason,
        "summary": summary
    }
