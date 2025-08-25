from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager, logout_user
import os
from dotenv import load_dotenv
from models.user import User
from flask_mail import Mail

app_src_dir = os.path.dirname(__file__)
project_root_dir = os.path.dirname(app_src_dir)

load_dotenv(os.path.join(app_src_dir, '.env'))

app = Flask(__name__, template_folder=project_root_dir, static_folder=project_root_dir)

db_password = os.getenv('DB_PASSWORD')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = app.debug
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)


@login_manager.user_loader
def load_user(email: str) -> User | None:
    try:
        return User(**mongo.db.users.find_one({'email': email}))
    except TypeError:
        logout_user()
