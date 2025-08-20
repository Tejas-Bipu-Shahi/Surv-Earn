from pydantic import BaseModel
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    email: str
    password_hash: str
    username: str
    _id: str | None = None

    def get_id(self):
        return self.email


class TempUnverifiedUser(BaseModel):
    email: str
    password_hash: str
    username: str
    otp_hash: str
