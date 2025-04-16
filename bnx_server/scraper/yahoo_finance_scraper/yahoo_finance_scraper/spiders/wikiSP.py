import scrapy

class WikiSPSpider(scrapy.Spider):
    name = 'wiki_sp'
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    ]

    def __init__(self, pipeline=None, *args, **kwargs):
        super(WikiSPSpider, self).__init__(*args, **kwargs)
        self.pipeline = pipeline

    def parse(self, response):
        # Extracting stock symbols from the Wikipedia page
        symbols = []
        # rows = response.css('table.wikitable tbody tr')

        # for row in rows[1:]:  # Skip the header row
        #     symbol = row.css('td:nth-child(1) a::text').get()
        #     if symbol:
        #         # print("SYMBOL: ", symbol) 
        #         symbols.append(symbol)

        symbol = response.css('table.wikitable tbody tr td:nth-child(1) a::text').getall()  

        # for s in symbol:
        #     print("SYMBOL: ", s)
        # Process symbols in the pipeline
        if self.pipeline:
            # for symbol in symbols:
            self.pipeline.process_item(symbol, self)
        # yield symbols
        yield symbol
