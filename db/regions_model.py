from db.sql_main import BaseModel, get_session

from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, delete, and_, DATE

vin_reg = "Вінницька"
vol = "Волинська"
dnip = "Дніпропетровська"
donec = "Донецька"
gitom = "Житомирська"
zak = "Закарпатська"
zaporiz = "Запорізька"
ivano_franc = "Івано-Франківська"
kyiv = "Київська"
kirov = "Кіровоградська"
lug = "Луганська"
lviv = "Львівська"
mikol = "Миколаївська"
odess = "Одеська"
polt = "Полтавська"
rivn = "Рівненська"
sums = "Сумська"
tern = "Тернопільська"
hark = "Харківська"
hers = "Херсонська"
hmel = "Хмельницька"
cherk = "Черкаська"
chern = "Чернівецька"
cherni = "Чернігівська"

main_names = [vin_reg, vol, dnip, donec, gitom, zak, zaporiz, ivano_franc, kyiv, kirov, lug, lviv, mikol, odess, polt, rivn, sums, tern, hark, hers, hmel, cherk, chern, cherni]
platforma_volunteer_country_names = []
volonter_org_name = []
prykhystok_gov_ua_name = []
dopomagai_org_name = []


class RegionModel(BaseModel):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_name = Column(VARCHAR(45), primary_key=False, nullable=False)
    platforma_volunteer_country_name = Column(VARCHAR(45), primary_key=False, nullable=False)
    volonter_org_name = Column(VARCHAR(45), primary_key=False, nullable=False)
    prykhystok_gov_ua_name = Column(VARCHAR(45), primary_key=False, nullable=False)
    dopomagai_org_name = Column(VARCHAR(45), primary_key=False, nullable=False)

    def __init__(self, main_name: str, platforma_volunteer_country_name, volonter_org_name, prykhystok_gov_ua_name,
                 dopomagai_org_name):
        self.main_name = main_name
        self.platforma_volunteer_country_name = platforma_volunteer_country_name
        self.volonter_org_name = volonter_org_name
        self.prykhystok_gov_ua_name = prykhystok_gov_ua_name
        self.dopomagai_org_name = dopomagai_org_name

    def insert(self):
        session = get_session()
        session.add(self)
        session.commit()
