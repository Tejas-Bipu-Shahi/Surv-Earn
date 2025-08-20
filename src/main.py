from flask import request, render_template, redirect, url_for, flash, session
import bcrypt
from models.user import User, TempUnverifiedUser
import utils.functions as fn
from controllers import user_handler
from flask_login import login_required, login_user, logout_user, current_user

from config import app, mongo

# logging
from icecream import ic


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('user/dist/index.html')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if not fn.is_valid_email(email):
            return render_template('register.html', email_error='Invalid Email!', email=email, password=password,
                                   confirm_password=confirm_password, username=username)

        if mongo.db.users.find_one({'email': email}):
            return render_template('register.html', email_error='Email already in use.', email=email, password=password,
                                   confirm_password=confirm_password, username=username)

        if len(password) < 8:
            return render_template('register.html', password_error='Password must be at least 8 characters.', email=email,
                                   password=password, confirm_password=confirm_password, username=username)

        if password != confirm_password:
            return render_template('register.html', confirm_password_error='Passwords do not match.', email=email, password=password,
                                   confirm_password=confirm_password, username=username)

        temp_unverified_user = user_handler.create_temp_unverified_user(email=email, password=password, username=username, mongo=mongo)
        session['temp_unverified_email'] = temp_unverified_user.email
        return redirect(url_for('verify_otp'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # todo: if user is already logged in ask to logout first or logout automatically
    if request.method == 'POST':
        ic(request.form)

        email = request.form['email']
        password = request.form['password']

        if not fn.is_valid_email(email):
            return render_template('login.html', email_error='Invalid Email!', email=email, password=password)

        existing_user = mongo.db.users.find_one({'email': email})
        if not existing_user:
            return render_template('login.html', email_error='Email Not Found!', email=email, password=password)

        user: User = User(**existing_user)

        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return render_template('login.html', password_error='Incorrect Password!', email=email, password=password)

        ic(f'User {email} logged in.')

        if request.form.get('keep_logged_in'):
            login_user(user, remember=True)
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if current_user.is_authenticated:
        ic(f'User {current_user.email} logging out.')

        logout_user()

        ic(f'logout successful.')

        return redirect(url_for('index'))
    return 'Not logged in.'


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return f'Settings Page for {current_user.email}.'


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template('reset_password.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if not session.get('temp_unverified_email'):
        return "Not Allowed"
    if request.method == 'POST':
        email = session['temp_unverified_email']
        entered_otp = request.form['otp']
        temp_unverified_user_data = mongo.db.temp_unverified_users.find_one({'email': email})
        temp_unverified_user = TempUnverifiedUser(**temp_unverified_user_data)
        if not bcrypt.checkpw(entered_otp.encode(), temp_unverified_user.otp_hash.encode()):
            return render_template('verify_otp.html', otp_error='Incorrect OTP!')

        user_handler.register_user(
            email=temp_unverified_user.email,
            password_hash=temp_unverified_user.password_hash,
            username=temp_unverified_user.username,
            mongo=mongo
        )
        session.pop('temp_unverified_email')
        return redirect(url_for('login'))
    return render_template('verify_otp.html', email=session['temp_unverified_email'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
