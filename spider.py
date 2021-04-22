import scrapy
from shutil import which
from scrapy_selenium import SeleniumRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    a=2
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800
        },
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': 'C:\\Users\\me\\Downloads\\chromedriver_win32\\chromedriver.exe',
        'SELENIUM_DRIVER_ARGUMENTS': ['--headless']
    }

    def start_requests(self):
        urls = ['https://www.daraz.pk/smartphones/?page=2']
        for url in urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10)

    def parse(self, response):
        
        
        # print(response.selector.xpath("//div[@class='c16H9d']/a/text()").extract())

        for mobile in response.selector.xpath("//div[@class='c16H9d']"):
            
            print(mobile.xpath("a/text()").extract())
            yield {
                'mobile_name': mobile.xpath("a/text()").extract()
            }
            # print(quote)
        
        next_page = response.css("li[title='Next Page'] a::attr('href')").get()
        
        # if next_page is not None:
        yield response.follow(next_page, self.parse)
