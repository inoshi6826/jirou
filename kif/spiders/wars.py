import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import base64
import time


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

            time.sleep(3)
            # * canvasを画像として保存
            canvas = driver.find_element(By.ID, "main_game")

            id = canvas.get_attribute("id")
            path = f"./img/{id}.png"
            dataURLs = self.driver.execute_script(
                "return arguments[0].toDataURL('image/png').substring(21);", 
                canvas)
            image = base64.b64decode(dataURLs)
            with open(path, mode='wb') as f:
                f.write(image)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            print(soup)
            self.driver.quit()
