from db.sql_main import BaseModel, get_session

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, delete, and_, DATE


class VolunteerModel(BaseModel):
    __tablename__ = "volunteer_table"

    name = Column(VARCHAR(45), primary_key=True, nullable=False)
    date = Column(VARCHAR(45), primary_key=False, nullable=False)
    organizer = Column(VARCHAR(45), primary_key=False, nullable=True)
    region = Column(VARCHAR(45), primary_key=False, nullable=True) # replace with region
    url = Column(VARCHAR(45), primary_key=False, nullable=False)

    def __init__(self, name: str, date, organizer, region, url):
        self.name = name
        self.date = date
        self.organizer = organizer
        self.region = region
        self.url = url

    def insert(self):
        session = get_session()
        session.add(self)
        session.commit()
