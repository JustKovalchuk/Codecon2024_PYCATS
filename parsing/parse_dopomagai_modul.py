import time
from datetime import datetime

from db.accommodation_table import *
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Building:
    def __init__(self, location: str, people: int, date: str, link: str, dangers: list[str] = None, primarys: list[str] = None, info: str = None):
        self.location = location
        self.dangers = dangers
        self.primarys = primarys
        self.people = people
        self.info = info
        self.date = date
        self.link = link

    def save_to_sql(self):
        try:
            AccommodationModel(self.date, self.info, self.location, str(self.primarys), str(self.dangers), None, self.people, self.link).insert()
        except Exception as e:
            print(e)

    def Display(self):
        print("="*20)
        print(f"Location::{self.location}")
        print(f"Dangers::{self.dangers}")
        print(f"Primary::{self.primarys}")
        print(f"People::{self.people}")
        print(f"Info::{self.info}")
        print(f"Date::{self.date}")
        print(f"Url::{self.link}")


def parce_houses_dopomagai():
    url = "https://dopomagai.org/find"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    def parse_body():
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="__next"]/div[1]/ws-block/section/div/div[2]/div[2]/div/*/div/div[@class="card-body"]'))
        )
        result = []
        for element in elements:
            location = element.find_element(By.XPATH,'.//div/h4/b').text
            tmp_elements = element.find_element(By.XPATH,'.//div[3]')

            dangers = tmp_elements.find_elements(By.CLASS_NAME,'bg-danger')
            primarys = tmp_elements.find_elements(By.CLASS_NAME,'bg-primary')

            people = element.find_element(By.XPATH, './/p[1]/b').text.split(": ")[1]
            info = element.find_element(By.XPATH, './/p[2]').text
            date = element.find_element(By.XPATH, './/p[3]').text.split("Створено: ")[1]
            list_dangers = []
            for i in dangers:
                list_dangers.append(i.text)
            list_primarys = []
            for i in primarys:
                list_primarys.append(i.text)

            btn = element.find_element(By.CLASS_NAME,'dropdown-toggle')
            while True:
                try:
                    btn.click()
                    url = element.find_element(By.CLASS_NAME, 'dropdown-item')
                    break
                except:
                    ...
            url.click()
            link = pyperclip.paste()
            result.append(Building(location=location,dangers=list_dangers,primarys=list_primarys,people=people,info=info,date=date,link=link))
        return result

    def scroll():
        while True:
            try:
                scroll_btn = driver.find_element(By.CLASS_NAME, 'get-next-page_wrapper__rFUvt')
                scroll_btn.click()
                break
            except:
                ...

    for i in range(2):
        scroll()
        time.sleep(1)
    result = parse_body()

    driver.quit()
    return result
