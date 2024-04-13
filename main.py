import asyncio
import logging
import sys
from db.sql_main import set_con, create_connection, get_session
from db.volunteer_table import VolunteerModel

from datetime import datetime
from Parsing.platforma_volunteer import get_events

from bot.misc import main
set_con(create_connection("localhost", "root", "123987MySQL_", "codecon"))

if __name__ == "__main__":

    event_location = input("Enter the location (e.g., Lviv): ")
    events = get_events(location=event_location)
    for event in events:
        event.save_to_sql()
        event.show()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
