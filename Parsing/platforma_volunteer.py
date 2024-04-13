import re

import requests
from bs4 import BeautifulSoup

from db.volunteer_table import VolunteerModel


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


def get_events():
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


if __name__ == '__main__':
    events = get_events()
    s = []
    print(len(events))
    for event in events:
        s.append(event.location)

    s = list(set(s))
    print(s)
    print(len(s))
