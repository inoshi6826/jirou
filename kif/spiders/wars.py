from logging import raiseExceptions
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import re


class WarsSpider(scrapy.Spider):
    name = "wars"
    allowed_domains = ["shogiwars.heroz.jp"]

    start_urls = ["https://shogiwars.heroz.jp/loginm/WEBAPP_24ea8c24-53df-4987-baeb-baddc4663cad/ed53ccbec94dfd40159726ea9b36ca53220b0c8e?version=webapp_7.1.0_standard&locale=ja"]
    game_header = "http://shogiwars.heroz.jp/games/"
    account = "splash111"
    password = "magic111"

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
            login_area = driver.find_element(By.CLASS_NAME, "login_area")
            input = login_area.find_elements(By.TAG_NAME, "input")  
            name_flg = False
            psw_flg = False
            for item in input:
                name = item.get_attribute("name")
                if name == "name":
                    item.send_keys(self.account)
                    name_flg = True
                elif name == "password":
                    item.send_keys(self.password)
                    psw_flg = True
                elif name == "commit":
                    if name_flg == True and psw_flg == True:
                        try:
                            print("clicking item")
                            item.click()
                        except:
                            driver.quit()
                            raise Exception("for some reason login function was denied.")
                else:
                    print(name)
            time.sleep(3)
            try:
                ok_btn = driver.find_element(By.CLASS_NAME, "alertable-ok")
                ok_btn.click()
            except:
                driver.quit()
                raise Exception("ok btn not found")
            print(driver.page_source)
            # * マイページの処理
            a = driver.find_element(By.XPATH, "//*[@id='record']/div[7]/a[2]")
            a.click()
            # * ここから履歴ページの処理
            time.sleep(1)
            tenmin_btn = driver.find_element(By.ID, "ten_min_tab")
            tenmin_btn.click()
            WebDriverWait(driver, timeout=3).until(driver.find_element(By.CLASS_NAME, "contents"))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            list = soup.find("div", attrs={"id": "list"})
            for item in list:
                kif_ls = soup.find_all("div", class_="game_replay")
                for kif in kif_ls:
                    incomplete_url = kif.a["onclick"]
                    game_id = re.sub("appAnalysis|\(|'|\)", "", incomplete_url)
                    game_url = self.game_header + game_id
                    print(game_url)
            self.driver.quit()
