# Define your item pipelines here
from itemadapter import ItemAdapter


class BlogCrawlerPipeline:
    def process_item(self, item, spider):
        return item
