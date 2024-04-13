from db.sql_main import BaseModel, get_session

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, delete, and_, DATE
from sqlalchemy.dialects.mysql import insert


class VolunteerModel(BaseModel):
    __tablename__ = "volunteer_table"

    name = Column(VARCHAR(255), primary_key=True, nullable=False)
    date = Column(VARCHAR(45), primary_key=False, nullable=False)
    organizer = Column(VARCHAR(45), primary_key=False, nullable=True)
    region = Column(VARCHAR(45), primary_key=False, nullable=True) # replace with region
    url = Column(VARCHAR(255), primary_key=False, nullable=False)

    def __init__(self, name: str, date, organizer, region, url):
        self.name = name
        self.date = date
        self.organizer = organizer
        self.region = region
        self.url = url

    def insert(self):
        try:
            session = get_session()
            session.add(self)
            session.commit()
        except Exception as e:
            print("cant insert", e)
