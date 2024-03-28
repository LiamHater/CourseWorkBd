import os
import random
from datetime import datetime

from mimesis.builtins import RussiaSpecProvider
from mimesis.locales import Locale
from mimesis import Person, Gender, Address
from random import choice
from database import Database
from dotenv import load_dotenv


def make_person():
    genders = ["male", "female"]
    gender = Gender(choice(genders))
    person = Person(locale=Locale.RU)
    provider = RussiaSpecProvider()
    return {
        "имя": person.name(gender=gender),
        "фамилия": person.surname(gender=gender),
        "отчество": provider.patronymic(gender=gender),
        "номер_документа": int(provider.series_and_number().replace(" ", "")),
    }


def add_years(start_date, years):
    try:
        return start_date.replace(year=start_date.year + years)
    except ValueError:
        # 👇️ preserve calendar day (if Feb 29th doesn't exist, set to 28th)
        return start_date.replace(year=start_date.year + years, day=28)


def make_passport(number):
    person = Person()
    birthdate = person.birthdate(max_year=2009)

    organizations = ["умвд россии по хабаровскому краю",
                     "какая-то организация"]

    passport = {
        "номер_документа": number,
        "дата_выдачи": add_years(birthdate, 14),
        "кем_выдан": choice(organizations),
        "дата_рождения": birthdate,
        "фото_налогоплательщика": open("../placeholders/unknownPerson.jpg", "rb").read(),
    }

    return passport


def make_taxes_declaration(passport: int, inspection: int):
    address_gen = Address(locale=Locale.RU)
    address = address_gen.address().split()
    house = address[-1]
    street = address[1]

    return {
        "город": address_gen.city(),
        "улица": street,
        "дом": house,
        "район_проживания": address_gen.state(),
        "номер_документа": passport,
        "номер_инспекции": inspection
    }


def add_person_with_passport(db: Database):
    person = make_person()
    passport = make_passport(person["номер_документа"])

    db.insert_query("документ_удостоверяющий_личность", tuple(passport.keys()), tuple(passport.values()))
    db.insert_query("налогоплательщик", tuple(person.keys()), tuple(person.values()))


def make_inspection():
    return {
        "название_инспекции": "Инспекция" + str(datetime.now().day) + str(datetime.now().microsecond)
    }


def add_inspection(db: Database):
    inspection = make_inspection()
    db.insert_query("инспекции", tuple(inspection.keys()), tuple(inspection.values()))


def add_declaration(db: Database):
    index = choice(db.select_query("инспекции", columns="id_инспекции"))
    passport = choice(db.select_query("документ_удостоверяющий_личность", columns="номер_документа"))
    declaration = make_taxes_declaration(passport, index)

    db.insert_query("налоговая_декларация", tuple(declaration.keys()), tuple(declaration.values()))


def main():
    db = Database(os.getenv("DATABASE_PASSWORD"))
    # add_person_with_passport(db)


if __name__ == "__main__":
    load_dotenv()
    # main()
    db = Database(os.getenv("DATABASE_PASSWORD"))

