from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from models.user import User

app_src_dir = os.path.dirname(__file__)
project_root_dir = os.path.dirname(app_src_dir)

load_dotenv(os.path.join(app_src_dir, '.env'))

app = Flask(__name__, template_folder=project_root_dir, static_folder=project_root_dir)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/SurvUsersTestDB'
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email: str) -> User:
    return User(**mongo.db.users.find_one({'email': email}))
