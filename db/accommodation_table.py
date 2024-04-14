from db.sql_main import BaseModel, get_session

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, delete, and_, DATE, Text


class AccommodationModel(BaseModel):
    __tablename__ = "accommodation_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(VARCHAR(255), primary_key=False, nullable=False)
    desc = Column(Text(535), primary_key=False, nullable=False)
    region = Column(VARCHAR(255), primary_key=False, nullable=False) # replace with region
    accepted = Column(VARCHAR(535), primary_key=False, nullable=True)
    term = Column(VARCHAR(255), primary_key=False, nullable=True)
    accommodation_type = Column(VARCHAR(255), primary_key=False, nullable=True)
    number_of_people = Column(Integer, primary_key=False, nullable=True)
    url = Column(VARCHAR(255), primary_key=False, nullable=False)

    def __init__(self, date, desc, region, accepted, term, accommodation_type, number_of_people, url):
        self.date = date
        self.desc = desc
        self.region = region
        self.accepted = accepted
        self.term = term
        self.accommodation_type = accommodation_type
        self.number_of_people = number_of_people
        self.url = url

    def lv_string(self, index) -> str:
        d1 = str(self.accepted).replace("'", "").replace("[", "").replace("]", "")
        d2 = str(self.term).replace("'", "").replace("[", "").replace("]", "")
        d3 = str(self.accommodation_type).replace("'", "").replace("[", "").replace("]", "")

        date = str(self.date).split(" ")[0]
        txt = (
            f" 🔸 <b>Пропозиція №{index}</b>\n"
            f"    Кількість осіб: {self.number_of_people}\n"
            f"    Локація: {self.region}\n"
            f"    Кого приймають: {d1}\n"
            f"    На який термін: {d2}\n")
        if self.accommodation_type:
            txt += f"    Тип розміщення: {d3}\n"
        # content = as_list(
        #     as_marked_section(
        #         Text(Bold(f"{index}"), ". ", Bold(self.desc), ":"),
        #         Text(Bold("Локація"), f": {self.region}"),
        #         Text(Bold("Дата"), f": {self.date}"),
        #         marker="   ",
        #     ),
        # )
        return txt

    def full_string(self, index) -> str:
        d1 = str(self.accepted).replace("'", "").replace("[", "").replace("]", "")
        d2 = str(self.term).replace("'", "").replace("[", "").replace("]", "")
        d3 = str(self.accommodation_type).replace("'", "").replace("[", "").replace("]", "")

        date = str(self.date).split(" ")[0]
        txt = (
            f"<b>Пропозиція №{index}</b>\n"
            f"   🔸 <b>Опис</b>: {self.desc}\n"
            f"   🔸 <b>Кількість осіб</b>: {self.number_of_people}\n"
            f"   🔸 <b>Локація</b>: {self.region}\n"
            # f"   🔸 <b>Дата</b>: {date}\n"
            f"   🔸 <b>Кого приймають</b>: {d1}\n"
            f"   🔸 <b>На який термін</b>: {d2}"
            )

        if self.accommodation_type:
            txt += f"\n   🔸 <b>Тип розміщення</b>: {d3}"
        txt += f"\n\nПовна інформація за посиланням 👉 {self.url}"
        return txt

    def insert(self):
        session = get_session()
        session.add(self)
        session.commit()

    @staticmethod
    def find_by_location(name):
        data = get_session().query(AccommodationModel).filter(AccommodationModel.region.like(f'%{name}%')).all()
        return data

    @staticmethod
    def close_session():
        get_session().close()
