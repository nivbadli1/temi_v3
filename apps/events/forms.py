# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired


class EventForm(FlaskForm):
    eventID = StringField('eventID', validators=[DataRequired()])







