import bcrypt
from models.user import User

# type hinting
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask_pymongo import PyMongo

# logging
from icecream import ic


def register_user(email: str, password: str, mongo: 'PyMongo') -> User:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user: User = User(email=email, password=hashed_password.decode())
    mongo.db.users.insert_one(user.model_dump())

    ic(user)

    return user
