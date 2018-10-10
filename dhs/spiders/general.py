# -*- coding: utf-8 -*-
import scrapy
import pudb
#pudb.set_trace()

# Define configuration
PAGES = 3
BASE_URL = 'https://ltclicensing.oregon.gov/Facilities?page=2&RangeValue=50&AFH=True&ALF=True&NF=True&RCF=True&Medicaid=True&Medicare=True&PrivatePay=True&OpenOnly=False'
URL_INIT = "https://ltclicensing.oregon.gov"
CONFIG = {
    'results': '//tr[@class="clickable-row"]',
    'pages': '//tr[@class="clickable-row"]',
    'open':
    {
        'facility_name':['//td[1]/text()'],
        'city':['//td[2]/text()'],
        'url':['//tr/@data-href'],
        'type':['//td[3]/text()'],
        'beds':['//td[4]/text()'],
        'funding_source':['//td[5]/text()'],
        'status':['//td[6]/text()'],

    },
    'nested':
    {
        'raw_text': ['//div[@id="facilityTab"]//div[@class="col-md-5"]/text()']

    }
}

def fetch_data(_res_sel, product, config, level):
    '''
    extracts dict data from single row
    '''
    for key,value in config[level].items():
       for _item in value:
           x_val = _res_sel.xpath(_item).extract()
           if len(x_val)>0:
               product[key] = x_val[0].strip()
               break
    return product

class GeneralSpider(scrapy.Spider):
    name = 'general'
    allowed_domains = ['ltclicensing.oregon.gov']
    start_urls = ['']
    def start_requests(self):
        for _page in range(1, (PAGES+1)):
            url = BASE_URL + "&page=" + str(_page)
            request = scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            request.meta['page'] = _page
            yield request

    def parse(self, response):
        ''' extract initial table '''
        _page = response.request.meta['page']
        results = response.xpath(CONFIG['results']).extract()
        for _res in results:
            item = {}
            item['page'] = _page
            _sel = scrapy.Selector(text=_res, type='html')
            item = fetch_data(_sel, item, CONFIG, 'open')
            url = URL_INIT + item['url']
            request = scrapy.Request(url=url, callback=self.parse_final, dont_filter=True)
            request.meta['item'] = {** item }
            yield request

    def parse_final(self, response):
        ''' extracts inner data (street and zip) '''
        item = response.request.meta['item']
        nested_raws = response.xpath(CONFIG['nested']['raw_text'][0]).extract()
        nested_raw = [_raw.strip() for _raw in nested_raws if _raw.strip()!='']
        item['street'], item['zip'] = nested_raw[0], nested_raw[-1]
        yield item
