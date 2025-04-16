import scrapy

class YahooSPSpider(scrapy.Spider):
    name = 'yahoo_sp'
    start_urls = [
        'https://finance.yahoo.com/quote/%5ESPX/',
    ]

    def __init__(self, pipeline=None, *args, **kwargs):
        super(YahooSPSpider, self).__init__(*args, **kwargs)
        self.pipeline = pipeline

    def parse(self, response):
        item = {

            'value': response.css('section.yf-16vvaki span[data-testid="qsp-price"]::text').get(),

            # Change from previous trading day or the last close
            'change': response.css('section.yf-16vvaki span[data-testid="qsp-price-change"]::text').get(),

            # relative change in the index value compared to the previous close
            'relativeChange': response.css('section.yf-16vvaki span[data-testid="qsp-price-change-percent"]::text').get(),

            'timeDate': response.css('section.yf-16vvaki span.yf-vednlp span::text').get(),

            'previousClose': response.css('div[data-testid="quote-statistics"] ul li:nth-child(1) span fin-streamer::text').get(),

            'open': response.css('div[data-testid="quote-statistics"] ul li:nth-child(2) span fin-streamer::text').get(),

            'volume': response.css('div[data-testid="quote-statistics"] ul li:nth-child(3) span fin-streamer::text').get(),

            'daysRange': response.css('div[data-testid="quote-statistics"] ul li:nth-child(4) span fin-streamer::text').get(),

            'yearWeekRange': response.css('div[data-testid="quote-statistics"] ul li:nth-child(5) span fin-streamer::text').get(),

            'avgVolume': response.css('div[data-testid="quote-statistics"] ul li:nth-child(6) span fin-streamer::text').get(),

        }

        if self.pipeline:
            self.pipeline.process_item(item, self)
        yield item