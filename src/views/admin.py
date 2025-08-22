from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import current_user, login_required
import os
from datetime import date

from config import project_root_dir, mongo
from models.survey import Survey, SurveyStatus

from icecream import ic

admin_bp = Blueprint(name='admin', import_name=__name__, url_prefix='/admin',
                     static_folder=os.path.join(project_root_dir, 'admin', 'dist'),
                     template_folder=os.path.join(project_root_dir, 'admin', 'dist'))


@admin_bp.route('/accountsettings', methods=['GET', 'POST'])
@login_required
def accountsettings():
    if not current_user.is_admin:
        return "You are not an Admin."
    return render_template('accountSettings.html')


@admin_bp.route('/addsurvey', methods=['GET', 'POST'])
@login_required
def addsurvey():
    if not current_user.is_admin:
        return "You are not an Admin."
    if request.method == 'POST':
        survey_title = request.form['survey-title']
        survey_short_desc = request.form['survey-short']
        reward = request.form['reward']
        expiry_date = request.form['expiry-date']
        est_time = request.form['est-time']
        form_url = request.form['form-url']
        no_of_questions = request.form['num-questions']
        category = request.form['category']

        company_name = 'N/A'

        survey = Survey(survey_title=survey_title, company_name=company_name, reward_per_completion=float(reward), survey_url=form_url,
                        short_description=survey_short_desc, status=SurveyStatus.ACTIVE, estimated_time=int(est_time),
                        date_posted=date.today(), questions_count=int(no_of_questions), category=category,
                        expiration_date=date.fromisoformat(expiry_date))
        ic(survey)

        mongo.db.surveys.insert_one(survey.model_dump())

    return render_template('addSurvey.html')


@admin_bp.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    if not current_user.is_admin:
        return "You are not an Admin."
    return render_template('changePassword.html')


@admin_bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if not current_user.is_admin:
        return "You are not an Admin."
    return render_template('payment.html')


@admin_bp.route('/surveydetails', methods=['GET', 'POST'])
@login_required
def surveydetails():
    if not current_user.is_admin:
        return "You are not an Admin."
    return render_template('surveyDetails.html')


@admin_bp.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    if not current_user.is_admin:
        return "You are not an Admin."
    return render_template('transaction.html')


@admin_bp.route('/yoursurveys', methods=['GET', 'POST'])
@login_required
def yoursurveys():
    if not current_user.is_admin:
        return "You are not an Admin."
    return render_template('yourSurveys.html')


@admin_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    if not current_user.is_admin:
        return "You are not an Admin."
    return "notification"
