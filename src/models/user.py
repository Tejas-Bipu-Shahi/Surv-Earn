from pydantic import BaseModel
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    email: str
    password: str

    def get_id(self):
        return self.email
