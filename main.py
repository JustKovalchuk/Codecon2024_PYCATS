import asyncio
import logging
import sys
from db.sql_main import set_con, create_connection, get_session
from db.volunteer_table import VolunteerModel

from datetime import datetime

from bot.misc import main
set_con(create_connection("localhost", "root", "123987MySQL_", "codecon"))

if __name__ == "__main__":
    # VolunteerModel("Name", str(datetime.now()), "Organizer", "Region", "Url")
    # VolunteerModel("Name", str(datetime.now()), "Organizer", "Region", "Url")
    # VolunteerModel("Name1", str(datetime.now()), "Organizer", "Region", "Url")
    # get_session()
    session = get_session()
    session.add(VolunteerModel("Name", str(datetime.now()), "Organizer", "Region", "Url"))
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
