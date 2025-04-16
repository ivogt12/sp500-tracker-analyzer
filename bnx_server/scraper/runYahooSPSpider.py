import scrapy
import json
from scrapy.crawler import CrawlerProcess
from yahoo_finance_scraper.yahoo_finance_scraper.pipelines import YahooFinanceScraperPipeline
from yahoo_finance_scraper.yahoo_finance_scraper.spiders.yahoo_sp import YahooSPSpider

def run_spider():
    pipeline = YahooFinanceScraperPipeline()
    process = CrawlerProcess()

    process.crawl(YahooSPSpider, pipeline=pipeline)
    process.start()  # The script will block here until the crawling is finished

    print(json.dumps(pipeline.get_data(), indent=4))  # Print the data in a readable format

    # return pipeline.get_data()

if __name__ == '__main__':
    scraped_data = run_spider()
    # print(scraped_data)  # Print the data or save it to a file
