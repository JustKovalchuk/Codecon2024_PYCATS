from db.sql_main import BaseModel, get_session

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, delete, and_, DATE


class AccommodationModel(BaseModel):
    __tablename__ = "accommodation_table"

    name = Column(VARCHAR(45), primary_key=True, nullable=False)
    date = Column(VARCHAR(45), primary_key=False, nullable=False)
    region = Column(VARCHAR(45), primary_key=False, nullable=True) # replace with region
    accepted = Column(VARCHAR(45), primary_key=False, nullable=True)
    term = Column(VARCHAR(45), primary_key=False, nullable=True)
    accommodation_type = Column(VARCHAR(45), primary_key=False, nullable=True)
    url = Column(VARCHAR(45), primary_key=False, nullable=False)

    def __init__(self, name: str, date, desc, region, accepted, term, accommodation_type, url):
        self.name = name
        self.date = date
        self.desc = desc
        self.region = region
        self.accepted = accepted
        self.term = term
        self.accommodation_type = accommodation_type
        self.url = url

    def insert(self):
        session = get_session()
        session.add(self)
        session.commit()

    def delete(self):
        session = get_session()
        session.delete(self)
        session.commit()

    @staticmethod
    def find_by_location(name):
        data = get_session().query(AccommodationModel).filter(AccommodationModel.region.like(f'%{name}%')).all()
        return data