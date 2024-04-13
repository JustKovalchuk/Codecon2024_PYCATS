from db.sql_main import BaseModel, get_session

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, delete, and_, DATE
from sqlalchemy.dialects.mysql import insert

from aiogram.utils.formatting import as_list, as_marked_section, Bold, Text


class VolunteerModel(BaseModel):
    __tablename__ = "volunteer_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
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

    def lv_string(self, index) -> str:
        # content = as_list(
        #     as_marked_section(
        #         Text(Bold(f"{index}"), ". ", Bold(self.name), ":"),
        #         Text(Bold("Локація"), f": {self.region}"),
        #         Text(Bold("Дата"), f": {self.date}"),
        #         marker="   🔸 ",
        #     ),
        # )
        str = (
            f"{index}. <b>{self.name}</b>:\n"
            f"   🔸 <b>Локація</b>: {self.region}\n"
            f"   🔸 <b>Дата</b>: {self.date}\n")
        return str

    def full_string(self, index) -> str:
        # content = as_list(
        #     as_marked_section(
        #         Text(Bold(f"{index}"), ". ", Bold(self.name), ":"),
        #         Text(Bold("Локація"), f": {self.region}"),
        #         Text(Bold("Дата"), f": {self.date}"),
        #         Text(Bold("Організатор"), f": {self.organizer}\n"
        #                                   f"\nПовна інформація за посиланням -> {self.url}"),
        #         marker="   🔸 ",
        #     ),
        # )
        str = (
            f"{index}. <b>{self.name}</b>:\n"
            f"   🔸 <b>Локація</b>: {self.region}\n"
            f"   🔸 <b>Дата</b>: {self.date}\n"
            f"   🔸 <b>Організатор</b>: {self.organizer}\n"
            f"   🔸 <b>Дата</b>: {self.date}\n\n"
            f"Повна інформація за посиланням -> {self.url}")
        return str

    def insert(self):
        try:
            session = get_session()
            session.add(self)
            session.commit()
        except Exception as e:
            print("cant insert")

    @staticmethod
    def find_by_location(name):
        data = get_session().query(VolunteerModel).filter(VolunteerModel.region.like(f'%{name}%')).all()
        return data

    @staticmethod
    def get_all():
        session = get_session()
        return session.query(VolunteerModel).all()

    @staticmethod
    def close_session():
        get_session().close()