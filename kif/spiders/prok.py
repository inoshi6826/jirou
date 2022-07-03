import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..items import ProKifItem
from bs4 import BeautifulSoup


class ProkSpider(scrapy.Spider):
    name = "prok"
    allowed_domains = ["shogidb2.com"]
    start_urls = ["http://shogidb2.com/newrecords/"]

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    DRIVER_PATH = "chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    counter = 1
    """
    def parse_next_page(self):
        self.counter += 1
        print(self.counter)
        url = self.start_urls[0] + "page/" + str(self.counter)
        yield scrapy.Request(url, self.parse)
    """
    def parse(self, response):
        try:
            url = response.url
        except:
            url = self.start_urls[0]
        href_ls = []
        driver = self.driver

        driver.get(url)
        als = driver.find_elements(By.CLASS_NAME, "list-group-item")
        for a in als:
            href = a.get_attribute("href")
            href_ls.append(href)

        print(href_ls)
        for ref in href_ls:
            driver.get(ref)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            container = soup.find("div", class_="container-fluid")
            script = container.script
            # * kif data
            kif_data = script.text
            name_data = driver.find_element(By.CLASS_NAME, "h2")
            # * title
            name = name_data.text

            yield ProKifItem(name=name, url=ref, data=kif_data)

        driver.get(url)
        target_url = (
            "https://shogidb2.com/games/fc30edb2e83a7667e81072930f987643d6794b4d"
        )

        if target_url not in href_ls:
            print("Got the target url.")
            self.counter += 1
            print(self.counter)
            url = self.start_urls[0] + "page/" + str(self.counter)
            yield scrapy.Request(url, self.parse)
        else:
            print("----------------------------------------")
            print("mission accomplished!")
            print("----------------------------------------")
            
            driver.quit()
