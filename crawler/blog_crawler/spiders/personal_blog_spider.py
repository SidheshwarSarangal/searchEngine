"""import scrapy
from blog_crawler.items import BlogCrawlerItem

class PersonalBlogSpider(scrapy.Spider):
    name = 'personal_blog'
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            item = BlogCrawlerItem()
            item['title'] = quote.css('span.text::text').get()
            item['author'] = quote.css('small.author::text').get()
            item['date'] = ''  # Not available on this site
            item['content'] = quote.css('span.text::text').get()
            item['url'] = response.url
            yield item
"""

import scrapy
from blog_crawler.items import BlogCrawlerItem

class PersonalBlogSpider(scrapy.Spider):
    name = 'personal_blog'
    start_urls = ['https://food-dee-dum.com/']  # Starting from homepage

    def parse(self, response):
        # If there are blog post links, follow them
        for link in response.css('a::attr(href)').getall():
            if '/p/' in link or '/posts/' in link:
                yield response.follow(link, callback=self.parse_post)

        # Also scrape this page itself
        yield from self.parse_post(response)

    def parse_post(self, response):
        # Make sure URL belongs to your domain
        if 'food-dee-dum.com' not in response.url:
            return

        item = BlogCrawlerItem()
        item['title'] = response.css('h1.entry-title::text').get()
        item['author'] = response.css('.author a::text').get() or ''
        item['date'] = response.css('time.entry-date::attr(datetime)').get() or ''
        item['content'] = ' '.join(response.css('div.entry-content p::text').getall()).strip()
        item['url'] = response.url
        yield item
