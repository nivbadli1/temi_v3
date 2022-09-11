# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired

from apps.authentication.models import Patient
from apps.patients.utils import get_days_list


class EventForm(FlaskForm):
    eventID = StringField('eventID', validators=[DataRequired()])


class AddNewEventForm(FlaskForm):
    # patient_list = get_patients_list
    patient_list = SelectField('מטופל', choices=[], validators=[DataRequired()])
    contact_list = SelectField('איש קשר', choices=[], validators=[DataRequired()])
    day = SelectField('יום', choices=get_days_list(), validators=[DataRequired()])
#     event_hour_start = SelectField('משעה', choices=get_hour_list(), validators=[DataRequired()])





