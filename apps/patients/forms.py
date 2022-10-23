# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired
from apps.patients import utils

from apps.authentication import forms
from apps.patients.utils import get_days_list, get_times_list


# login and registration

class PatientForm(FlaskForm):
    patient_id = StringField('תעודת זהות', validators=[DataRequired()])
    f_name = StringField('שם פרטי', validators=[DataRequired()])
    l_name = StringField('שם משפחה', validators=[DataRequired()])
    bed = IntegerField('מיקום מיטה', validators=[DataRequired()])
    department = IntegerField('מספר מחלקה', validators=[DataRequired()])
    max_calls = IntegerField('מספר שיחות שבועיות', validators=[DataRequired()])
    select_list = SelectField('idates', validators=[DataRequired()])

class ContactForm(FlaskForm):
    f_name = StringField('שם פרטי', validators=[DataRequired()])
    l_name = StringField('שם משפחה', validators=[DataRequired()])
    phone = StringField('מספר טלפון', validators=[DataRequired()])
    mail = StringField('כתובת מייל', validators=[DataRequired()])
    priority = IntegerField('עדיפות', validators=[DataRequired()])
    day = DateField(id='datepick')


class ContactTimeForm(FlaskForm):
    # option_widget = widget.
    day = SelectField('יום', choices=get_days_list(),coerce=str,option_widget={"selected":"3"})
    from_hour = SelectField('משעה', choices=get_times_list(), validators=[DataRequired()])
    to_hour = SelectField('עד שעה', choices=get_times_list(), validators=[DataRequired()])
