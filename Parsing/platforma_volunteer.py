import re

from db.volunteer_table import VolunteerModel
import requests
from bs4 import BeautifulSoup


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


def get_events(location):
    events_ = []
    base_url = 'https://platforma.volunteer.country'
    event_url = base_url + f"/events?keywords={location}"

    response = requests.get(event_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        divs = soup.find_all('div', class_='events--card--content')

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
            if organiser_element.find('a'):
                ev_organiser = organiser_element.find('a').find('div').find('div',
                                                                         class_='organization--lettermark--name sm').text.strip()

            _event = Event(name=event_name, date=event_date, location=location, organiser=ev_organiser, link=event_link)
            events_.append(_event)

        return events_
    else:
        print(f"Failed to retrieve data from {event_url}")
        return None


if __name__ == '__main__':
    event_location = input("Enter the location (e.g., Lviv): ")
    events = get_events(location=event_location)
    for event in events:
        event.save_to_sql()
        event.print()