import bcrypt
from models.user import User, TempUnverifiedUser
from utils.otp_generator import generate_otp

# type hinting
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask_pymongo import PyMongo

# logging
from icecream import ic


def register_user(email: str, password_hash: str, username: str, mongo: 'PyMongo') -> User:
    user: User = User(email=email, password_hash=password_hash, username=username)
    mongo.db.users.insert_one(user.model_dump())

    ic(f'Registered: {user}')

    return user


def create_temp_unverified_user(email: str, password: str, username: str, mongo: 'PyMongo') -> TempUnverifiedUser:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    otp = generate_otp()
    otp_hash = bcrypt.hashpw(otp.encode(), bcrypt.gensalt())
    temp_unverified_user: TempUnverifiedUser = TempUnverifiedUser(email=email, password_hash=password_hash.decode(), username=username,
                                                                  otp_hash=otp_hash.decode())
    mongo.db.temp_unverified_users.insert_one(temp_unverified_user.model_dump())

    ic(otp)  # send otp via email
    ic(f'Created Unverified User: {temp_unverified_user}')

    return temp_unverified_user
