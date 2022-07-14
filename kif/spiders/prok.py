import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..items import ProKifItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


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
        driver.implicitly_wait(30)
        driver.get(url)
        als = driver.find_elements(By.CLASS_NAME, "list-group-item")
        for a in als:
            href = a.get_attribute("href")
            href_ls.append(href)

        print(href_ls)
        for ref in href_ls:
            driver.implicitly_wait(30)
            driver.get(ref)
            # * title
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            title = element.text
            try:    
                # * kif data
                kif_export = driver.find_element(By.ID, "kif-export")
                kif_export.click()
                print(self.counter)
                kif_modal = driver.find_element(By.ID, "kifu-modal")
                target_word = "先手"
                WebDriverWait(kif_modal, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, "textarea"), target_word)
                )
                kif_data = kif_modal.find_element(By.TAG_NAME, "textarea").text
                yield ProKifItem(name=title, url=ref, data=kif_data)
            except:
                print("no kif data found in textarea")
                print("game title: " + title)
        driver.get(url)
        # ! about 700 pages
        target_url = "https://shogidb2.com/games/6892579e327663b07fc085eda3d9cc08fa3979e6"

        if target_url not in href_ls:
            print("Got the target url.")
            self.counter += 1
            url = self.start_urls[0] + "page/" + str(self.counter)
            yield scrapy.Request(url, self.parse)
            print("現在のページ: " + str(self.counter))
        else:
            print("----------------------------------------")
            print("mission accomplished!")
            print("----------------------------------------")
            
            driver.quit()
