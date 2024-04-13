import time

import selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime

from db.accommodation_table import AccommodationModel


class Residence:
    def __init__(self, date: datetime, address: str, region: str, number_of_places: int, link: str,
                 description: str = None,
                 settlers: list[str] = None, terms: list[str] = None, types_of_residence: list[str] = None):
        self.date = date
        self.address = address
        self.region = region
        self.number_of_places = number_of_places
        self.description = description
        self.settlers = settlers
        self.terms = terms
        self.types_of_residence = types_of_residence
        self.link = link

    def save_to_sql(self):
        try:
            AccommodationModel(self.date, self.description, self.address, str(self.settlers), str(self.terms), str(self.types_of_residence), self.link).insert()
        except Exception as e:
            print(e)

    def show(self):
        return


def get_accommodations():
    return get_accommodation_prykhystok()


def get_accommodation_prykhystok():
    base_url = 'https://prykhystok.gov.ua'
    # event_url = f'{base_url}/find?region={location}&persons={resident_number}'
    event_url = f"{base_url}/find?region&persons&persons_type="

    driver = webdriver.Firefox()
    driver.get(event_url)
    driver.maximize_window()

    def Parse_data():
        residences: list[Residence] = []
        divs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//div[@data-v-6fe561d6 and @data-v-8f389854 and @class='mb-4']/div/div/div[@class = 'b-overlay-wrap position-relative']")))
        for div in divs:
            try:
                settlers: list[str] = []
                terms: list[str] = []
                types_of_residence: list[str] = []
                line_counter = 0
                offer_text = div.text
                lines = offer_text.split('\n')
                if lines[0].startswith('О'):
                    line_counter += 1
                date_str = lines[line_counter].split(' ')[1]
                date = datetime.strptime(date_str, '%d.%m.%Y')
                address = lines[line_counter + 1]
                region = lines[line_counter + 2]
                number_of_places = int(lines[line_counter + 3].split(':')[1].strip())

                link = div.find_element(By.XPATH, "h3[@class = 'mb-2']/a").get_attribute('href')

                try:
                    description = div.find_element(By.XPATH, "p[@class='notes']").text
                except selenium.common.exceptions.NoSuchElementException:
                    print('No description')
                    description = ''
                detail_div = div.find_element(By.XPATH, "div[@class='d-flex flex-wrap']")

                try:
                    settler_spans = detail_div.find_element(By.CLASS_NAME, "persons").find_elements(By.TAG_NAME, "span")
                    for settler in settler_spans:
                        settlers.append(settler.text)
                except selenium.common.exceptions.NoSuchElementException:
                    print('No settlers')
                    settlers = ''

                try:
                    term_spans = detail_div.find_element(By.CLASS_NAME, "period").find_elements(By.TAG_NAME, "span")
                    for term in term_spans:
                        terms.append(term.text)
                except selenium.common.exceptions.NoSuchElementException:
                    terms = ''

                try:
                    type_spans = detail_div.find_element(By.CLASS_NAME, "accomodation-type").find_elements(By.TAG_NAME, "span")
                    for type in type_spans:
                        types_of_residence.append(type.text)
                except selenium.common.exceptions.NoSuchElementException:
                    types_of_residence = ''
                residences.append(Residence(date=date, address=address, region=region, number_of_places=number_of_places,
                                            description=description, settlers=settlers, terms=terms,
                                            types_of_residence=types_of_residence, link=link))
            except Exception as e:
                print("Skip")
        return residences

    def Update_site():
        old_count = len(driver.find_elements(By.XPATH,
                                             "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/*/div[1]"))
        cnt = 0
        while cnt < 10:
            cnt += 1
            # Move the cursor to the element and click on it
            button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Завантажити ще')]")[0]
            for i in range(3):
                try:
                    button.click()
                    time.sleep(1)
                except:
                    time.sleep(1)

            new_count = len(driver.find_elements(By.XPATH,
                                                 "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/*/div[1]"))
            if new_count == old_count:
                break
            old_count = new_count

    Update_site()
    offers = Parse_data()
    driver.quit()

    return offers
