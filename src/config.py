from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from models.user import User

load_dotenv('.env')

app = Flask(__name__, template_folder='../')
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/SurvUsersTestDB'
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email: str) -> User:
    return User(**mongo.db.users.find_one({'email': email}))
