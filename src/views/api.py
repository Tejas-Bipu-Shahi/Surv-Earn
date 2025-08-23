from flask import Blueprint, jsonify, request
from bson import ObjectId
from models.user import User
from models.survey import Survey
from config import mongo

from icecream import ic

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/surveysubmission', methods=['POST'])
def surveysubmission():
    mongo.db.surveysubmission.insert_one({
        'headers': list(request.headers.items()),
        'json': request.json
    })
    try:
        if request.json.get('data').get('fields')[-1].get('label') != 'email':
            # the last field of the form must be email field with label set to "email"
            return jsonify({
                'message': 'Email field not found. Please add email field with label "email" at the end of the form.',
                'status': 400
            })
        if not request.headers.get('surveyid'):
            return jsonify({
                'message': 'Survey id is required. Please add a header with key="survey_id" and value="<survey_id>".',
                'status': 400
            })
    except (AttributeError, TypeError):
        return jsonify({
            'message': 'Some attributes are not specified or incorrectly specified in the request.',
            'status': 400
        })

    survey_id = request.headers.get('surveyid')

    data: dict = request.json.get('data')
    fields = data.get('fields')

    ic(request.headers)
    ic(fields)

    email = fields[-1].get('value')  # last element should always be email

    userdata = mongo.db.users.find_one({'email': email})
    surveydata = mongo.db.surveys.find_one({'_id': ObjectId(survey_id)})
    if not userdata:
        return jsonify({
            'message': f'user {email} not found',
            'statuscode': 404,
        })
    if not surveydata:
        return jsonify({
            'message': f'survey {survey_id} not found',
            'statuscode': 404,
        })

    user = User(**userdata)
    survey = Survey(**surveydata)

    user.total_completed_surveys += 1
    user.current_balance += survey.reward_per_completion
    user.total_earnings += survey.reward_per_completion
    user.completed_surveys.append(survey.id)

    mongo.db.users.update_one({'email': email}, {'$set': userdata})

    return jsonify({
        'message': f'success',
        'statuscode': 200,
    })
