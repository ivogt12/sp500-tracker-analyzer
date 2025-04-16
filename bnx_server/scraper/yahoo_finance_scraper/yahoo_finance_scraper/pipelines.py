# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class YahooFinanceScraperPipeline:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def get_data(self):
        return self.data

class WikiSPScraperPipeline:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def get_data(self):
        return self.data

class YahooFinanceStockScraperPipeline:
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def get_data(self):
        return self.data