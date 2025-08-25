import os

from flask import request, render_template, redirect, url_for, flash, session
import bcrypt
from models.user import User, TempUnverifiedUser
import utils.functions as fn
from controllers import user_handler, email_sender
from flask_login import login_required, login_user, logout_user, current_user
from utils.otp_generator import generate_otp
from bson import ObjectId
from models.company_data import CompanyData
from config import app, mongo, mail

# logging
from icecream import ic


@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            users_count = mongo.db.users.count_documents({'is_admin': False})
            active_surveys_count = mongo.db.surveys.count_documents({})
            total_submissions_count = mongo.db.survey_submissions.count_documents({})
            company_data = CompanyData()
            return render_template('admin/dist/index.html', users_count=users_count,
                                   active_surveys_count=active_surveys_count,
                                   total_submissions_count=total_submissions_count,
                                   company_data=company_data)
        return render_template('user/dist/index.html')

    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Already Registered', 'warn')
        return "<h1>You are already registered and logged in.</h1>"
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if not fn.is_valid_email(email):
            flash('Invalid Email')
            return render_template('register.html', email_error='Invalid Email!', email=email, password=password,
                                   confirm_password=confirm_password, username=username)

        if mongo.db.users.find_one({'email': email}):
            flash('Already Registered', 'warn')
            return render_template('register.html', email_error='Email already in use.', email=email, password=password,
                                   confirm_password=confirm_password, username=username)

        if mongo.db.temp_unverified_users.find_one({'email': email}):
            mongo.db.temp_unverified_users.delete_one({'email': email})

        if len(password) < 8:
            return render_template('register.html', password_error='Password must be at least 8 characters.', email=email,
                                   password=password, confirm_password=confirm_password, username=username)

        if password != confirm_password:
            return render_template('register.html', confirm_password_error='Passwords do not match.', email=email, password=password,
                                   confirm_password=confirm_password, username=username)
        otp = generate_otp()
        otp_hash = bcrypt.hashpw(otp.encode(), bcrypt.gensalt())
        if request.form.get('register_as_admin'):
            recipient = os.getenv('PRIMARY_ADMIN_EMAIL')
            is_admin = True
        else:
            recipient = email
            is_admin = False

        temp_unverified_user = user_handler.create_temp_unverified_user(email=email, password=password, username=username,
                                                                        otp_hash=otp_hash.decode(), mongo=mongo, is_admin=is_admin)
        session['temp_unverified_email'] = temp_unverified_user.email

        status: tuple[bool, str] = email_sender.send_otp_mail(mail=mail, otp=otp, recipient=recipient,
                                                              sender=app.config.get('MAIL_DEFAULT_SENDER'))
        if not status[0]:
            ic(status[1])
            return render_template('register.html', email=email, password=password,
                                   confirm_password=confirm_password, username=username)
        flash('User Registered!', 'success')
        return redirect(url_for('verify_otp'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "<h1>You are already logged in!</h1>"
    if request.method == 'POST':
        ic(request.form)

        email = request.form['email']
        password = request.form['password']

        if not fn.is_valid_email(email):
            flash('Invalid Email!')
            return render_template('login.html', email_error='Invalid Email!', email=email, password=password)

        existing_user = mongo.db.users.find_one({'email': email})
        if not existing_user:
            flash('Email not found', 'error')
            return render_template('login.html', email_error='Email Not Found!', email=email, password=password)

        user: User = User(**existing_user)

        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            flash('Incorrect Password!', 'error')
            return render_template('login.html', password_error='Incorrect Password!', email=email, password=password)

        ic(f'User {email} logged in.')

        if request.form.get('keep_logged_in'):
            login_user(user, remember=True)
        else:
            login_user(user)
        flash('Login Successful!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if current_user.is_authenticated:
        ic(f'User {current_user.email} logging out.')
        flash('Logout Successful!', 'success')
        logout_user()

        ic(f'logout successful.', 'success')

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

    email = session['temp_unverified_email']
    temp_unverified_user_data = mongo.db.temp_unverified_users.find_one({'email': email})
    temp_unverified_user = TempUnverifiedUser(**temp_unverified_user_data)

    if request.method == 'POST':
        entered_otp = request.form['otp']

        if not bcrypt.checkpw(entered_otp.encode(), temp_unverified_user.otp_hash.encode()):
            return render_template('verify_otp.html', otp_error='Incorrect OTP!', email=email)

        user_handler.register_user(
            email=temp_unverified_user.email,
            password_hash=temp_unverified_user.password_hash,
            username=temp_unverified_user.username,
            mongo=mongo,
            is_admin=temp_unverified_user.is_admin
        )
        session.pop('temp_unverified_email')
        mongo.db.temp_unverified_users.delete_one({'email': temp_unverified_user.email})
        return redirect(url_for('login'))

    if temp_unverified_user.is_admin:
        otp_reciever = os.getenv('PRIMARY_ADMIN_EMAIL')
    else:
        otp_reciever = temp_unverified_user.email

    return render_template('verify_otp.html', email=otp_reciever)


@app.route('/fillsurvey', methods=['GET', 'POST'])
@login_required
def fillsurvey():
    surveys = list(mongo.db.surveys.find())
    total_surveys = len(surveys)
    return render_template('user/dist/fillSurvey.html', surveys=surveys, enumerate=enumerate, total_surveys=total_surveys)


@app.route('/surveyhistory', methods=['GET', 'POST'])
@login_required
def surveyhistory():
    return render_template('user/dist/survHistory.html', enumerate=enumerate, mongo=mongo, ObjectId=ObjectId)


@app.route('/redeems', methods=['GET', 'POST'])
@login_required
def redeem():
    return render_template('user/dist/redeem.html')


@app.route('/accountsettings', methods=['GET', 'POST'])
@login_required
def accountsettings():
    if request.method == 'POST':
        full_name = request.form['fullname']
        phone_number = request.form['phone']
        dob = request.form['birthday']
        address = request.form['address']
        zip_code = request.form['zipcode']
        occupation = request.form['occupation']
        gender = request.form['gender']
        city = request.form['city']
        education = request.form['education']

        user_updated_data = dict(full_name=full_name, phone_number=phone_number,
                                 dob=dob, address=address, zip_code=zip_code, occupation=occupation
                                 , gender=gender, city=city, education=education)

        mongo.db.users.update_one(dict(email=current_user.email),
                                  {"$set": user_updated_data})
        flash("Saved Successfully!", 'success')
        return redirect(url_for('accountsettings'))

    return render_template('user/dist/accountSettings.html')


@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    return render_template('user/dist/changePassword.html')


@app.route('/surveyDetails', methods=['GET', 'POST'])
@login_required
def surveydetails():
    survey_id = request.args.get('survey_id')
    if survey_id:
        survey = mongo.db.surveys.find_one({'_id': ObjectId(survey_id)})
    else:
        survey = None
    return render_template('user/dist/surveyDetails.html', survey=survey)


@app.route('/opensurveyurl', methods=['GET', 'POST'])
@login_required
def opensurveyurl():
    survey_id = request.args.get('survey_id')
    if survey_id:
        survey = mongo.db.surveys.find_one({'_id': ObjectId(survey_id)})
    else:
        survey = None
    ic(survey_id)
    ic(survey)
    if survey:
        return redirect(survey.get('survey_url'))
    return "Not Found"


@app.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    return render_template('user/dist/transaction.html')


@app.route('/notifications', )
@login_required
def notifications():
    return render_template('user/dist/notifications.html')


@app.route('/about')
def about():
    return render_template('/about.html')


if __name__ == '__main__':
    from views.admin import admin_bp
    from views.api import api_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.run(debug=True, port=5000, host='0.0.0.0')
