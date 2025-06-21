import scrapy
from blog_crawler.items import BlogCrawlerItem
from bs4 import BeautifulSoup
import re

class PersonalBlogSpider(scrapy.Spider):
    name = 'personal_blog'
    start_urls = [
        "https://www.atlassian.com/blog/announcements"
    ]

    def parse(self, response):
        yield from self.parse_post(response)

    def parse_post(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        # Title fallback
        title_tag = soup.find('h1')
        fallback_title = soup.get_text().strip().split("\n")[0][:60]

        # Extract author/date from meta
        author = (soup.find('meta', attrs={'name': 'author'}) or {}).get('content', '')
        date = (soup.find('meta', attrs={'property': 'article:published_time'}) or {}).get('content', '')

        # Save full HTML content instead of plain text
        full_html = response.text

        item = BlogCrawlerItem()
        item['title'] = title_tag.get_text(strip=True) if title_tag else fallback_title
        item['author'] = author
        item['date'] = date
        item['content'] = full_html.strip()  # Save raw HTML here
        item['url'] = response.url

        yield item
