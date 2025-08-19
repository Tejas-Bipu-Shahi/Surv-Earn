from flask import request, render_template
import bcrypt
from models.user import User
import utils.functions as fn
from controllers import user_handler
from flask_login import login_required, login_user, logout_user, current_user

from config import app, mongo

# logging
from icecream import ic


@app.route('/')
def index():
    if current_user.is_authenticated:
        return f'Welcome {current_user.email}'
    return '<h1>Welcome to Flask-Flask!. Please Register/Login.</h1>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if not fn.is_valid_email(email):
            return f'Invalid email {email}', 400

        if mongo.db.users.find_one({'email': email}):
            return f'{email} already exists. Please log in.'

        if len(password) < 8:
            return f'Password must be at least 8 characters long.'

        user = user_handler.register_user(email=email, password=password, mongo=mongo)
        return f"Registered {user.email}"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # todo: if user is already logged in ask to logout first or logout automatically
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not fn.is_valid_email(email):
            return f'Invalid email {email}', 400

        existing_user = mongo.db.users.find_one({'email': email})
        if not existing_user:
            return f'{email} does not exist. Please Register.'

        user: User = User(**existing_user)

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return f'Incorrect password.'

        ic(f'User {email} logged in.')

        # session['email'] = user.email
        login_user(user, remember=True)
        return f"Logged in {user.email}"

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if current_user.is_authenticated:
        ic(f'User {current_user.email} logging out.')

        logout_user()

        ic(f'logout successful.')

        return 'logout successful.'
    return 'Not logged in.'


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return f'Settings Page for {current_user.email}.'


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template('forgetpassword.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
