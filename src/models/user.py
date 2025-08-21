from pydantic import BaseModel
from flask_login import UserMixin
from datetime import date

from models.survey import Survey


class User(BaseModel, UserMixin):
    email: str
    password_hash: str
    username: str
    _id: str | None = None

    total_completed_surveys: int = 0
    current_balance: int = 0
    total_earnings: int = 0
    completed_surveys: list[Survey] = []

    full_name: str = ''
    phone_number: int | str = ''
    dob: date | str = ''
    address: str = ''
    zip_code: int | str = ''
    occupation: str = ''
    gender: str = ''
    city: str = ''
    education: str = ''

    def get_id(self):
        return self.email


class TempUnverifiedUser(BaseModel):
    email: str
    password_hash: str
    username: str
    otp_hash: str
