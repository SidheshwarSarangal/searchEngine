import ollama

def classify_blog_entry(entry, model="gemma:3b"):
    prompt = (
        f"Classify this blog content:\n"
        f"Title: {entry.get('title', '')}\n"
        f"Content: {entry.get('content', '')}\n"
        f"Author: {entry.get('author', '')}\n"
        f"Date: {entry.get('date', '')}\n"
        f"URL: {entry.get('url', '')}\n\n"
        f"Label it as one of: ['Personal', 'Corporate', 'Course', 'Ad', 'Other'] "
        f"and give a brief reason."
    )
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
