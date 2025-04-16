import json
from scrapy.crawler import CrawlerProcess
from yahoo_finance_scraper.yahoo_finance_scraper.pipelines import WikiSPScraperPipeline
from yahoo_finance_scraper.yahoo_finance_scraper.spiders.wikiSP import WikiSPSpider

def run_Wiki_SP_Spider():
    pipeline = WikiSPScraperPipeline()
    process = CrawlerProcess()

    process.crawl(WikiSPSpider, pipeline=pipeline)
    process.start()  # The script will block here until the crawling is finished

    print(json.dumps(pipeline.get_data(), indent=4))  # Print the data in a readable format

if __name__ == '__main__':
    scraped_data = run_Wiki_SP_Spider()