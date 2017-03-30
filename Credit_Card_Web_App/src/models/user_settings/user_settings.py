import src.models.user_settings.constants as SettingConstants
from src.common.database import Database
import uuid

class Settings():
    def __init__(self, user_email=None, billing_start_date=None, budget_amount=None, name=None, _id=None):
        self.user_email = user_email
        self.billing_start_date = billing_start_date
        self.budget_amount = budget_amount
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id


    def save_to_mongo(self):
        Database.update(SettingConstants.COLLECTION, {"user_email": self.user_email}, self.json())

    def json(self):
        return {
            #"_id": self._id,
            "user_email": self.user_email,
            "billing_start_date": self.billing_start_date,
            "budget_amount": self.budget_amount,
            "name": self.name
        }

    @classmethod
    def from_mongo(cls, user_email):
        user_email_settings = Database.find_one(SettingConstants.COLLECTION, query={'user_email': user_email})
        return cls(**user_email_settings)
