import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import re
from ..items import WarsItem as ITEM


class WarsSpider(scrapy.Spider):
    name = "wars"
    allowed_domains = ["shogiwars.heroz.jp"]
    start_urls = [
        "https://shogiwars.heroz.jp/loginm/WEBAPP_24ea8c24-53df-4987-baeb-baddc4663cad/ed53ccbec94dfd40159726ea9b36ca53220b0c8e?version=webapp_7.1.0_standard&locale=ja"
    ]
    game_header = "https://shogiwars.heroz.jp/games/"
    account = "splash111"
    password = "magic111"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    DRIVER_PATH = "chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.implicitly_wait(5)

    def select_game_type(self, type):
        driver = self.driver
        WebDriverWait(driver, timeout=3).until(
            driver.find_element(By.CLASS_NAME, "contents")
        )
        game_type_tab = driver.find_element(By.ID, "category_select_tab")
        game_types = game_type_tab.find_elements(By.TAG_NAME, "li")
        if type == "ten_min":
            ten_min = game_types[0]
            ten_min.click()
            return ten_min.text
        elif type == "three_min":
            three_min = game_types[1]
            return three_min.text
        elif type == "ten_sec":
            ten_sec = game_types[2]
            ten_sec.click()
            return ten_sec.text
        else:
            print("Not valid type. Will go with the default game type.")
            res = game_types[0]
            # ? res = game_type_tab.find_element(By.CLASS_NAME, "tab3.selected_tab")
            return res.text

    def parse_history(self, response):
        # * 履歴ページの処理
        driver = self.driver
        # game_typeはten_min, three_min, ten_secから選択。それ以外の場合10分。
        game_type = "three_min"
        current_game_type = self.select_game_type(game_type)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        list = soup.find("div", attrs={"id": "list"})
        for item in list:
            contents = item.find_all("div", class_="contents")
            # 各ゲームの情報取り出し
            for content in contents:
                kif = content.find("div", class_="game_replay")
                # ? 3切れ、10秒、10切れのいずれか
                type = content.find("div", class_="game_category").text
                # ? 日付
                date = content.find("div", class_="game_date").text
                # ! url取得
                incomplete_url = kif.a["onclick"]
                game_id = re.sub("appAnalysis|\(|'|\)", "", incomplete_url)
                game_url = self.game_header + game_id
                yield ITEM(url=game_url, type=type, date=date)
        # 次ページボタン
        WebDriverWait(driver, timeout=3).until(
            driver.find_element(By.CSS_SELECTOR("[rel='next']"))
        )
        pagination = driver.find_element(By.CLASS_NAME, "pagination")
        try:
            next_btn = pagination.find_element(By.CSS_SELECTOR("[rel='next']"))
            next_btn.click()
            next_url = next_btn.get_attribute("href")
            return scrapy.Request(next_url, callback=self.parse_history)
        except:
            print("No next btn found.")
            # note 一回の実行で10分、3分、10秒をそれぞれ解析する場合ここに追加。
            print("Ending the process.")
            self.driver.quit()

    def parse(self, response):
        name_flg = False
        psw_flg = False
        driver = self.driver
        for url in self.start_urls:
            driver.get(url)
            login_area = driver.find_element(By.CLASS_NAME, "login_area")
            input = login_area.find_elements(By.TAG_NAME, "input")
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
                            raise Exception(
                                "for some reason login function was denied."
                            )
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
            time.sleep(1)
            btns = driver.find_elements(By.CLASS_NAME, "common_button")
            for btn in btns:
                if btn.text == "対局結果・棋譜一覧":
                    btn.click()
                    break
            self.parse_history(response)
