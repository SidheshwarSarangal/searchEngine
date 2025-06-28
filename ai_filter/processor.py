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
    domain = urlparse(url).netloc.lower()

    # Personal blog whitelist
    blog_whitelist = [
    "firstround.com", "waitbutwhy.com", "manassaloi.com", "paulgraham.com",
    "nav.al", "highexistence.com", "lesswrong.com", "markmanson.net",
    "reactionwheel.net", "search.cpan.org"
    ]


    # Block non-HTML or structured file types
    non_html_ext = [".zip", ".pdf", ".text", ".txt", ".pptx", ".docx", ".tar.gz", ".7z"]
    if any(url.lower().endswith(ext) for ext in non_html_ext):
        return {
            "title": "Untitled", "author": "", "date": "", "url": url,
            "relevant": False,
            "reason": "Non-HTML or downloadable file.",
            "summary": ""
        }

    # Known irrelevant domains
    known_irrelevant_domains = [
        "cnn.com", "bbc.com", "nytimes.com", "reuters.com", "hbr.org",
        "indiatoday.in", "forbes.com", "businessinsider.com", "elle.com", "vogue.in"
    ]
    if domain in known_irrelevant_domains:
        return {
            "title": "Untitled", "author": "", "date": "", "url": url,
            "relevant": False,
            "reason": f"Domain '{domain}' is a known media/commercial site.",
            "summary": ""
        }

    html = fetch_url_content(url)
    if not html:
        return {
            "title": "Untitled", "author": "", "date": "", "url": url,
            "relevant": False,
            "reason": "Failed to fetch or empty content.",
            "summary": ""
        }

    cleaned = clean_html_content(html)
    soup = BeautifulSoup(html, "html.parser")
    page_title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"

    # Reject too short or weird content
    if not cleaned or len(cleaned.split()) < 50:
        return {
            "title": page_title, "author": "", "date": "", "url": url,
            "relevant": False,
            "reason": "Content too short or machine-generated.",
            "summary": ""
        }

    if cleaned.lstrip().startswith(("{", "<", "---")):
        return {
            "title": page_title, "author": "", "date": "", "url": url,
            "relevant": False,
            "reason": "Appears to be structured data (JSON/YAML/XML).",
            "summary": ""
        }

    trimmed = cleaned[:1200]

    # Soft keyword filters
    if domain not in blog_whitelist:
        promo_keywords = ["enroll", "bootcamp", "coaching", "certification", "sign up", "free trial"]
        landing_keywords = ["request demo", "platform features", "contact sales", "enterprise solution"]
        media_keywords = ["editorial team", "subscribe newsletter", "celebrity", "gossip", "trending now"]

        lower = cleaned.lower()
        if any(kw in lower for kw in promo_keywords):
            return {
                "title": page_title, "author": "", "date": "", "url": url,
                "relevant": False,
                "reason": "Appears to promote a course or product.",
                "summary": ""
            }
        if any(kw in lower for kw in landing_keywords):
            return {
                "title": page_title, "author": "", "date": "", "url": url,
                "relevant": False,
                "reason": "Looks like a company landing page.",
                "summary": ""
            }
        if any(kw in lower for kw in media_keywords):
            return {
                "title": page_title, "author": "", "date": "", "url": url,
                "relevant": False,
                "reason": "Reads like a media/lifestyle portal.",
                "summary": ""
            }

    # Final AI classification prompt
    prompt = f"""You're a blog classifier.

Given a web page's title and first 1200 characters of cleaned content, determine whether it's a **personal blog post** — not marketing, not company, not media.

Respond in **this exact JSON format**:
{{
  "relevant": true or false,
  "reason": "short reason",
  "summary": "brief 2-line summary"
}}

Mark "relevant": true ONLY if:
- It's a thoughtful, reflective blog post or article
- NOT commercial or promotional
- Written in a personal voice (first-person, subjective)
- NOT a landing page or company post
- NOT a news or SEO article

Title: {page_title}

Content:
{trimmed}
"""

    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        raw = response["message"]["content"].strip()

        if raw.startswith("```json"): raw = raw[7:]
        elif raw.startswith("```"): raw = raw[3:]
        if raw.endswith("```"): raw = raw[:-3]
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
