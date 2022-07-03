import scrapy
from selenium import webdriver


class WarsSpider(scrapy.Spider):
    name = "wars"
    allowed_domains = ["shogiwars.heroz.jp"]
    start_urls = ["http://shogiwars.heroz.jp/web_app/standard/"]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    DRIVER_PATH = "chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    def parse(self, response):
        for url in self.start_urls:
            self.driver.get(url)
            print(self.driver.page_source)
            self.driver.close()