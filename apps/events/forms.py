# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired
from apps.patients import utils

from apps.authentication import forms


class EventForm(FlaskForm):
    event_id = StringField('מספר אירוע', validators=[DataRequired()])







