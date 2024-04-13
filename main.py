import asyncio
import logging
import sys
from db.sql_main import set_con, create_connection, get_session
from db.volunteer_table import VolunteerModel
from db.accommodation_table import AccommodationModel
from db.regions_model import RegionModel

from configparser import ConfigParser

from Parsing import platforma_volunteer, Prykhystok

from bot.misc import main

config = ConfigParser()
config.read("config.ini")

server = config["DB"]["server"]
user = config["DB"]["user"]
password = config["DB"]["password"]
database = config["DB"]["database"]

logging.basicConfig(level=logging.INFO)

set_con(create_connection(server, user, password, database))

if __name__ == "__main__":
    try:
        # Parse platforma_volunteer
        events_platforma_volunteer = platforma_volunteer.get_events_platform_volunteer()
        for event in events_platforma_volunteer:
            event.save_to_sql()
        logging.info("platforma_volunteer parser completed successfully.")
        VolunteerModel.close_session()

        # Parse Prykhystok
        events_prykhystok = Prykhystok.get_accommodation_prykhystok()
        for event in events_prykhystok:
            event.save_to_sql()
        logging.info("Prykhystok parser completed successfully.")
        AccommodationModel.close_session()

        # Parse SeleniumModul
        events_selenium_modul = platforma_volunteer.get_events_from_volunteer_org()
        for event in events_selenium_modul:
            event.save_to_sql()
        logging.info("volunteer_org parser completed successfully.")
        VolunteerModel.close_session()

    except Exception as e:
        logging.error(f"Error occurred: {e}")

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
