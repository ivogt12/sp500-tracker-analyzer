import scrapy
import sys
import json
from scrapy.crawler import CrawlerProcess
from yahoo_finance_scraper.yahoo_finance_scraper.pipelines import YahooFinanceStockScraperPipeline
from yahoo_finance_scraper.yahoo_finance_scraper.spiders.yahoo_stock import YahooSPStockSpider

def run_spider(symbol):
    pipeline = YahooFinanceStockScraperPipeline()
    process = CrawlerProcess()

    # Pass the symbol to the spider
    process.crawl(YahooSPStockSpider, symbol=symbol, pipeline=pipeline)
    process.start()  # The script will block here until the crawling is finished
    
    print(json.dumps(pipeline.get_data(), indent=4))  # Print the data in a readable format
    # process.stop()
if __name__ == '__main__':
    if len(sys.argv) > 1:
        stock_symbol = sys.argv[1]  # Get the symbol from command-line arguments
        scraped_data = run_spider(stock_symbol)
    else:
        print("No stock symbol provided.")