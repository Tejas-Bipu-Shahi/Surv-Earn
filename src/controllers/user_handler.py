import bcrypt
from models.user import User, TempUnverifiedUser

# type hinting
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask_pymongo import PyMongo

# logging
from icecream import ic


def register_user(email: str, password: str, mongo: 'PyMongo', username: str) -> User:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user: User = User(email=email, password=hashed_password.decode(), username=username)
    mongo.db.users.insert_one(user.model_dump())

    ic(f'Registered: {user}')

    return user


def create_temp_unverified_user(email: str, password: str, mongo: 'PyMongo', username: str) -> TempUnverifiedUser:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    temp_unverified_user: TempUnverifiedUser = TempUnverifiedUser(email=email, password=hashed_password.decode(), username=username)
    mongo.db.temp_unverified_users.insert_one(temp_unverified_user.model_dump())

    ic(f'Created Unverified User: {temp_unverified_user}')

    return temp_unverified_user
