# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired

from apps.authentication.models import Patient
from apps.events.functions import generate_days_list
from apps.patients.utils import get_days_list


class EventForm(FlaskForm):
    eventID = StringField('eventID', validators=[DataRequired()])


class AddNewEventForm(FlaskForm):
    patient = SelectField('שם דייר/ת', choices=[], validators=[DataRequired()])
    contact = SelectField('איש קשר של הדייר/ת', choices=[], validators=[DataRequired()])
    day = SelectField('יום השיחה', choices=[], validators=[DataRequired()])
    time = SelectField('שעת השיחה', choices=[], validators=[DataRequired()])
