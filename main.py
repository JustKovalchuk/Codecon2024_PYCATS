import asyncio
import logging
import sys
from db.sql_main import set_con, create_connection, get_session
from db.volunteer_table import VolunteerModel

from datetime import datetime
from Parsing.ParseDopomogaModul import get_events as ge
from Parsing.platforma_volunteer import get_events

from bot.misc import main
set_con(create_connection("localhost", "root", "123987MySQL_", "codecon"))

if __name__ == "__main__":
    events = get_events(location="Львів")
    events = ge()
    for event in events:
        event.save_to_sql()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
