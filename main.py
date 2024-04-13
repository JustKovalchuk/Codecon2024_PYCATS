import asyncio
import logging
import sys
from db.sql_main import set_con, create_connection, get_session
from db.volunteer_table import VolunteerModel

from configparser import ConfigParser

from datetime import datetime
from Parsing.platforma_volunteer import get_all_volunteers
from Parsing.Prykhystok import get_accommodations

from bot.misc import main

config = ConfigParser()
config.read("config.ini")

server = config["DB"]["server"]
user = config["DB"]["user"]
password = config["DB"]["password"]
database = config["DB"]["database"]

set_con(create_connection(server, user, password, database))

if __name__ == "__main__":
    # events = get_all_volunteers()
    # for event in events:
    #     event.save_to_sql()
    accommodations = get_accommodations()
    for accommodation in accommodations:
        accommodation.save_to_sql()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
