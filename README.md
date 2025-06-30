# Search Engine for Blogs and Articles.
This project is done under GDSC @IIT Roorkee. The problem statement was to create a search engine which only shows good and useful personal blogs and article. There should be no course selling pages, advertisement pages or any generic advice pages. The team members are - 
- Sidheshwar Sarangal
- Gamit Krupal
- Ayan
---
## Description
The project consists of 5 parts -
- Crawler
- Ai Filter
- Push To Database
- Backend
- Frontend

### Crawler
The crawler is used to crawl over the internet to get a list of web page links. It uses Breadth-first-search approach. It goes to the web page of the given link and crawl over that web page document, where it finds new links. Then it goes throgh the webpages of those links and this process continues. Along with moving to the different pages, it saves its links and if any saved link comes again then it is not added to the list and we do not move to that again. With this go through the links till we get no more new links and all such unique links are saved. To run this -
- We have to put a link of a website(or several links) in the seed_urls.txt in crawler folder.
- In the root we have to do this -
  1. Move to the crawler folder
      `cd crawler`
  3. And run
     `scrapy crawl link_collector`
     
With this we will get a list of links in file collected_links.json in output folder in crawler.

### AI Filter
This is used prepare a list of links with their link url, summary, author(if present), date(if present) and to mark the useful and relevant links (personal blogs, articles and useful webpages) as true and also put the reason. We are using AI Model Gemma3:1b which is put in our systems with help of ollama. It uses the list created above which is the output of crawler. The prompt we are using is this -
``` You're a blog classifier.
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
```
There are certain other parameters as well such as domain checking, size of the web page document and declining media(image/audio/video) links. Also we check only first 1000 charaters as Gemma3:1b as it will make the task complete faster.
To run this -
- In the root we have to do this in terminal -
  1. Move to the crawler folder `cd ai_filter`
  2. Run command `python main.py`
We will get the list in the output folder in the file named filtered_data.json.

### 
