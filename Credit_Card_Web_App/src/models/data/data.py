import uuid
import re

import pymongo

from src.common.database import Database
import src.models.data.constants as DataConstants
from src.models.user_settings.user_settings import Settings
import datetime

class Data():
    def __init__(self, user_email, price, date, description=None, category=None, _id=None):
        self.user_email = user_email
        self.price = price
        self.date = date
        self.description = description
        self.category = category
        self._id = uuid.uuid4().hex if _id is None else _id


    def save_to_mongo(self):
        Database.insert(DataConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "user_email": self.user_email,
            "date": self.date,
            "price": self.price,
            "description": self.description,
            "category": self.category
        }

    @classmethod
    def from_mongo(cls, user_email):
        user_email_data = Database.find_one(DataConstants.COLLECTION, query={'user_email': user_email})
        return cls(**user_email_data)

    @staticmethod
    def from_email(user_email):
        return [data for data in Database.find(DataConstants.COLLECTION, query={'user_email': user_email})]

    @classmethod
    def test(cls, user_email):
        user_email_data = Database.find(DataConstants.COLLECTION, query={'user_email': user_email})
        return cls(**user_email_data)

    @staticmethod
    def prices_amount1(user_email):
        test = [data for data in Database.find_price(DataConstants.COLLECTION, query={'user_email': user_email})]
        for test in test:
            print(test)

    @classmethod
    def prices_amount(cls, user_email):
        user_email_data = [cls(**elem) for elem in Database.find(DataConstants.COLLECTION, query={'user_email': user_email})]
        amount = 0
        for amount_one in user_email_data:
            amount += amount_one.price
        return amount

    @staticmethod
    def test(user_email):
        date = Settings.from_mongo(user_email)
        user_date = date.billing_start_date
        year = user_date[0:4]
        month = user_date[5:7]
        day = user_date[8:10]
        year_int = int(year)
        month_int = int(month)
        day_int = int(day)
        my_time = datetime.date(year_int, month_int, day_int)
        delta = my_time + datetime.timedelta(days=7)
        first_date = my_time.strftime('%b %d')
        second_date = delta.strftime('%b %d')

        return first_date + ' - ' +second_date

    @staticmethod
    def user_amount_weekly(user_email):
        amount = Settings.from_mongo(user_email)
        user_monthly_amount = amount.budget_amount
        int_user_monthly_amount = int(user_monthly_amount)
        weekly = int_user_monthly_amount / 4

        return weekly

    @staticmethod
    def user_amount_monthly(user_email):
        amount = Settings.from_mongo(user_email)
        user_monthly_amount = amount.budget_amount
        int_user_monthly_amount = int(user_monthly_amount)
        return int_user_monthly_amount
