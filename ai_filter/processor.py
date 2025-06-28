import json
import re
import ollama
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clean_html_content(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text)

def fetch_url_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, timeout=10, headers=headers)
        if res.status_code == 200:
            return res.text
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
    return ""

def classify_blog_url(url, model="gemma3:1b"):
    domain = urlparse(url).netloc

    # Step 1: Domain blacklist
    known_irrelevant_domains = [
        "www.supermarketnews.com", "www.nytimes.com", "www.cnn.com",
        "www.forbes.com", "www.businessinsider.com", "www.reuters.com",
        "www.bbc.com", "hbr.org"
    ]
    if domain in known_irrelevant_domains:
        return {
            "title": "Untitled",
            "author": "",
            "date": "",
            "url": url,
            "relevant": False,
            "reason": f"Domain '{domain}' is a known news/corporate site.",
            "summary": ""
        }

    # Step 2: Fetch content
    html = fetch_url_content(url)
    if not html:
        return {
            "title": "Untitled",
            "author": "",
            "date": "",
            "url": url,
            "relevant": False,
            "reason": "Failed to fetch or empty content.",
            "summary": ""
        }

    cleaned = clean_html_content(html)
    trimmed = cleaned[:1500]

    # Step 3: Title extraction
    soup = BeautifulSoup(html, "html.parser")
    page_title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"

    # Step 4: Prefilter for obvious promotions
    promo_keywords = [
        "enroll now", "join the course", "placement support", "free trial",
        "live classes", "cohort", "certification", "bootcamp", "coaching", "sign up"
    ]
    if any(kw in cleaned.lower() for kw in promo_keywords):
        return {
            "title": page_title,
            "author": "",
            "date": "",
            "url": url,
            "relevant": False,
            "reason": "Page appears to promote a course or service.",
            "summary": ""
        }

    # Step 5: AI prompt
    prompt = f"""You're an AI classifier. Determine whether the given web page is a personal blog post or not.

Respond ONLY with this exact JSON format:
{{
  "relevant": true or false,
  "reason": "short reason",
  "summary": "2-line summary"
}}

Mark "relevant": true ONLY IF ALL of these are true:
- Content is a reflective, opinion-based blog or article
- NOT promoting or selling anything (courses, services, products)
- NOT a landing page or commercial website
- Written in personal voice (first/second person) and not SEO/funnel content
- From an individual, not a company or coaching brand

Title: {page_title}

Content:
{trimmed}
"""

    try:
        ai_response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        raw = ai_response["message"]["content"].strip()

        # Strip markdown formatting if present
        if raw.startswith("```json"):
            raw = raw[7:]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]

        raw = re.sub(r'[\x00-\x1F]+', ' ', raw)
        parsed = json.loads(raw)

        return {
            "title": page_title,
            "author": "",
            "date": "",
            "url": url,
            "relevant": parsed.get("relevant", False),
            "reason": parsed.get("reason", "").strip(),
            "summary": parsed.get("summary", "").strip()
        }

    except Exception as e:
        return {
            "title": page_title,
            "author": "",
            "date": "",
            "url": url,
            "relevant": False,
            "reason": f"AI classification failed: {e}",
            "summary": ""
        }
