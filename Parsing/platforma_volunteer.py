import re

import requests
from bs4 import BeautifulSoup

from db.volunteer_table import VolunteerModel
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Event:
    def __init__(self, name: str, date: str, location: str, link: str,
                 organiser: str = ''):
        self.name = name
        self.date = date
        self.organiser = organiser
        self.location = location
        self.link = link

    def save_to_sql(self):
        VolunteerModel(self.name, self.date, self.organiser, self.location, self.link).insert()

    def print(self):
        print(self.name, self.date, self.organiser, self.location, self.link)
        return [self.name, self.date, self.organiser, self.location, self.link]


def get_events_platform_volunteer():
    events = []
    base_url = "https://platforma.volunteer.country/events?filtered_categories%5B%5D=19&filtered_categories%5B%5D=33&filtered_categories%5B%5D=21&keywords=&page={}"

    i = 1
    while True:
        event_url = base_url.format(i)

        response = requests.get(event_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            divs = soup.find_all('div', class_='events--card--content')
            if len(divs) == 0:
                break
            for div in divs:
                event_name = div.find('div', class_='events--card--title').find('h2').text.strip()
                event_link = base_url + div.find('div', class_='events--card--title').find('a').get('href')

                event_date_str = div.find('div', class_='events--card--date-location-wrapper').find('div',
                                                                                                    class_='events--card--date').text.strip()

                match = re.search(r'\d{4}', event_date_str[::-1])
                year_index = len(event_date_str) - match.end()
                event_date = event_date_str[:year_index + 4]
                ev_location = div.find('div', class_='events--card--date-location-wrapper').find('div',
                                                                                                 class_='events--card--location tippy').text.strip()
                organiser_element = div.find('div', class_='organization--lettermark--wrapper sm')
                ev_organiser = None
                if organiser_element.find('a'):
                    ev_organiser = organiser_element.find('a').find('div').find('div',
                                                                                class_='organization--lettermark--name sm').text.strip()

                _event = Event(name=event_name, date=event_date, location=ev_location, organiser=ev_organiser, link=event_link)
                events.append(_event)
        else:
            print(f"Failed to retrieve data from {event_url}")
            break
        i += 1

    return events


def get_events_from_volunteer_org():
    parse_category = ["Армія", "Переселенці"]
    url = "https://volonter.org/dopomoga-volonterski-proekty"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div/div/section/div[2]/ul')))

    li_elements = element.find_elements(By.TAG_NAME, "li")

    for li in li_elements:
        name_element = li.find_element(By.CLASS_NAME, "text").text.lower()
        for category in parse_category:
            if category and name_element == category.lower():
                li.click()
    search_btn = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div/section/div[3]/a[2]')
    search_btn.click()

    time.sleep(2)

    flag = True
    name_and_url = []
    while flag:
        try:
            more_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/div/div/section/div[4]/a")))
            more_btn.click()
        except:
            flag = False
            name_elements = driver.find_elements(By.XPATH, '//*[@id="wrapper"]/div/div/section/div[3]/*/div/h3')
            for i in name_elements:
                tmp_data = {"name": "", "url": ""}
                tmp_name_element = i.find_element(By.TAG_NAME, 'a')
                tmp_url = tmp_name_element.get_attribute("href")
                tmp_data["name"] = tmp_name_element.text
                tmp_data["url"] = tmp_url
                name_and_url.append(tmp_data)
    info_results = []

    for i in name_and_url:
        driver.get(i['url'])

        tmp_element = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[1]/ul')
        tmp = tmp_element.find_elements(By.TAG_NAME, 'li')
        owner = driver.find_element(By.CLASS_NAME, 'author-name')
        info_results.append(Event(i['name'], tmp[0].text, tmp[1].text, i['url'], owner.text))

    driver.quit()

    return info_results


def get_all_volunteers():
    return get_events_platform_volunteer() + get_events_from_volunteer_org()


if __name__ == '__main__':
    events = get_events_platform_volunteer()
    s = []
    print(len(events))
    for event in events:
        s.append(event.location)

    s = list(set(s))
    print(s)
    print(len(s))
