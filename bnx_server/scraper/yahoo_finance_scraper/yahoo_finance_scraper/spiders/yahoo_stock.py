import scrapy

class YahooSPStockSpider(scrapy.Spider):
    name = 'yahoo_stock'
    
    def __init__(self, symbol=None, *args, **kwargs):
        super(YahooSPStockSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.base_url = 'https://finance.yahoo.com/quote/'

    def start_requests(self):
        endpoints = {
            'overview': '',
            'historical': '/history',
            'key_statistics': '/key-statistics',
            'balance_sheet': '/balance-sheet',
            'cash_flow': '/cash-flow',
            'financials': '/financials'
        }

        headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                       'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                       'Chrome/112.0.0.0 Safari/537.36')
    }
        
        for key, endpoint in endpoints.items():
            url = f'{self.base_url}{self.symbol}{endpoint}'
            # Map endpoints to different parse functions if needed
            callback = getattr(self, f'parse_{key}', self.parse)
            yield scrapy.Request(url, headers=headers, callback=callback, dont_filter=False)

    def parse_overview(self, response):
        # Parse the overview page if needed
        # Example: scrape the S&P 500 data metrics
        pass

    def parse_historical(self, response):
        # Parse historical stock performance data
        pass

    def parse_key_statistics(self, response):
        # Parse financial ratios
        financialRatiosInfo = {
            'trailingPeRatio': response.css('table.yf-kbx2lo tbody tr:nth-child(1) td:nth-child(2)::text').get(),
            'forwardPeRatio': response.css('table.yf-kbx2lo tbody tr:nth-child(2) td:nth-child(2)::text').get(),
            'pbRatio': response.css('table.yf-kbx2lo tbody tr:nth-child(3) td:nth-child(2)::text').get(),
            'roe': response.css('table.yf-kbx2lo tbody tr:nth-child(4) td:nth-child(2)::text').get(),
            'roa': response.css('table.yf-kbx2lo tbody tr:nth-child(5) td:nth-child(2)::text').get(),
            'debtToEquity': response.css('table.yf-kbx2lo tbody tr:nth-child(6) td:nth-child(2)::text').get(),
        }
        if self.pipeline:
            self.pipeline.process_item(financialRatiosInfo, self)
        yield financialRatiosInfo

    def parse_balance_sheet(self, response):
        balanceSheetInfo = {
            'totalAssets': response.css('section.yf-9ft13 div.tableBody div:nth-child(1) div:nth-child(3)::text').get(),
            'totalLiabilities': response.css('section.yf-9ft13 div.tableBody div:nth-child(2) div:nth-child(3)::text').get(),
            'shareholderEquity': response.css('section.yf-9ft13 div.tableBody div:nth-child(5) div:nth-child(2)::text').get(),
        }
        if self.pipeline:
            self.pipeline.process_item(balanceSheetInfo, self)
        yield balanceSheetInfo

    def parse_cash_flow(self, response):
        cashFlowInfo = {
            'operatingCashFlow': response.css('section.yf-9ft13 div.tableBody div.row:nth-child(1) div:nth-child(3)::text').get(),
            'investingCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(2) div:nth-child(3)::text').get(),
            'financingCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(3) div:nth-child(3)::text').get(),
            'freeCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(12) div:nth-child(2)::text').get(),
        }
        if self.pipeline:
            self.pipeline.process_item(cashFlowInfo, self)
        yield cashFlowInfo

    def parse_financials(self, response):
        # Example: scraping Revenue vs. Net Income Growth data
        revIncomeGrowthInfo = {
            'date': response.xpath('//section[contains(@class,"yf-9ft13")]//div[contains(@class,"tableHeader")]//div[contains(@class,"row")]/div[position()>=2 and position()<=6]/text()').getall(),
            'totalRevenue': response.xpath('//section[contains(@class,"yf-9ft13")]//div[contains(@class,"tableBody")]//div[1]/div[position()>=2 and position()<=6]/text()').getall(),
            'netIncomeCommStockHolders': response.xpath('//section[contains(@class,"yf-9ft13")]//div[contains(@class,"tableBody")]//div[10]/div[position()>=2 and position()<=6]/text()').getall(),
        }
        processed_data = self.process_financial_data(revIncomeGrowthInfo)

        yield processed_data

    def process_financial_data(self, data):
        # Process the financial data as needed
        # For example, you can store each metric separately or perform additional calculations
        if self.pipeline:
            # Process each key in the data dictionary
            for key, value in data.items():
                if isinstance(value, list):
                    # Handle list data (e.g., store, log, etc.)
                    self.pipeline.process_item({key: value}, self)
                else:
                    # Handle single object data if necessary
                    self.pipeline.process_item({key: value}, self)

        # Optionally yield the processed data
        return data


    def parse(self, response):
        # Default parser
        pass

    def close(self, reason):
        self.logger.info(f"Spider closed: {reason}")




# import scrapy

# class YahooSPStockSpider(scrapy.Spider):
#     name = 'yahoo_sp'

#     def __init__(self, symbol=None, *args, **kwargs):
#         super(YahooSPStockSpider, self).__init__(*args, **kwargs)
#         self.symbol = symbol

#     def start_requests(self):
#         # Construct the URL using the symbol
#         url = f'https://finance.yahoo.com/quote/{self.symbol}'
#         yield scrapy.Request(url, self.parse)

#     def parse(self, response):

#         # Data to be scraped:

#         # TODO: 1. Historical Stock Performance (Line Chart)
#         # Date, Close Price
#         # TODO: This data should be retrieved in another spider. 
#         # url: quote/symbol/history

#         # 2. Financial Ratios Comparison (Bar Chart)
#         # P/E Ratio, P/B Ratio, Return on Equity (ROE), Return on Assets (ROA), 
#         # Debt-to-Equity Ratio
#         # url: quote/symbol/key-statistics

#         # 3. Cash Flow and Balance Sheet Analysis (Stacked Bar Chart)
#         # Total Assets, Total Liabilities, Shareholder Equity, Operating Cash Flow,
#         # Investing Cash Flow, Financing Cash Flow, Free Cash Flow
#         # url: quote/symbol/balance-sheet
#         # url: quote/symbol/cash-flow

#         # 4. Revenue vs. Net Income Growth (Dual-Axis Line Chart)
#         # Date, Total Revenue, Net Income
#         # url: quote/symbol/financials

#         # Retrieved from quote/symbol/financials
#         revIncomeGrowthInfo = {

#             'date': response.css('section.yf-9ft13 div.tableHeader div.row div:nth-child(2-6)').getall(),

#             'totalRevenue': response.css('section.yf-9ft13 div.tableBody div:nth-child(1) div:nth-child(2-6)::text').getall(),

#             'netIncomeCommStockHolders': response.css('section.yf-9ft13 div.tableBody div:nth-child(10) div:nth-child(2-6)::text').getall(),
            
#         }

#         # Retrieved from quote/symbol/key-statistics
#         financialRatiosInfo = {
#             'trailingPeRatio': response.css('table.yf-kbx2lo tbody tr:nth-child(1) td::text').getall(),
#             'forwardPeRatio': response.css('table.yf-kbx2lo tbody tr:nth-child(2) td::text').getall(),
#             'pbRatio': response.css('table.yf-kbx2lo tbody tr:nth-child(2) td::text').getall(),
#             'roe': response.css('table.yf-kbx2lo tbody tr:nth-child(3) td::text').getall(),
#             'roa': response.css('table.yf-kbx2lo tbody tr:nth-child(4) td::text').getall(),
#             'debtToEquity': response.css('table.yf-kbx2lo tbody tr:nth-child(5) td::text').getall(),
#         }

#         # Retrieved from quote/symbol/cash-flow
#         cashFlowInfo = {
#             'operatingCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(1) div:nth-child(2)::text').get(),
#             'investingCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(2) div:nth-child(2)::text').get(),
#             'financingCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(3) div:nth-child(2)::text').get(),
#             'freeCashFlow': response.css('section.yf-9ft13 div.tableBody div:nth-child(12) div:nth-child(2)::text').get(),
#         }

#         # Retrieved from quote/symbol/balance-sheet
#         balanceSheetInfo = {
#             'totalAssets': response.css('section.yf-9ft13 div.tableBody div:nth-child(1) div:nth-child(2)::text').get(),

#             'totalLiabilities': response.css('section.yf-9ft13 div.tableBody div:nth-child(2) div:nth-child(2)::text').get(),

#             'shareholderEquity': response.css('section.yf-9ft13 div.tableBody div:nth-child(5) div:nth-child(2)::text').get(),
#         }
        
#         if self.pipeline:
#             self.pipeline.process_item(item, self)
#         yield item
