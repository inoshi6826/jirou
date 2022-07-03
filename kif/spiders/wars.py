import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


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
    driver.implicitly_wait(5)

    def parse(self, response):
        driver = self.driver
        for url in self.start_urls:
            driver.get(url)
            print(self.driver.page_source)
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            print(soup)
            self.driver.quit()
