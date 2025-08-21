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
    completed_surveys: list[Survey] | None = None

    full_name: str | None = None
    phone_number: int | None = None
    dob: date | None = None
    address: str | None = None
    zip_code: int | None = None
    occupation: str | None = None
    gender: str | None = None
    city: str | None = None
    education: str | None = None

    def get_id(self):
        return self.email


class TempUnverifiedUser(BaseModel):
    email: str
    password_hash: str
    username: str
    otp_hash: str
