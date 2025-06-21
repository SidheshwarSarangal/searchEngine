# Scrapy settings for blog_crawler project

BOT_NAME = "blog_crawler"

SPIDER_MODULES = ["blog_crawler.spiders"]
NEWSPIDER_MODULE = "blog_crawler.spiders"

ADDONS = {}


ROBOTSTXT_OBEY = True


FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    'output/blog_data.json': {
        'format': 'json',
        'encoding': 'utf8',
        'overwrite': True
    }
}

