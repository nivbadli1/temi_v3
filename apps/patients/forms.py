# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField
from wtforms.validators import Email, DataRequired
from apps.patients import utils
from apps.authentication import forms


# login and registration

class PatientForm(FlaskForm):
    patient_id = StringField('תעודת זהות',validators=[DataRequired()])
    f_name = StringField('שם פרטי',validators=[DataRequired()])
    l_name = StringField('שם משפחה',validators=[DataRequired()])
    bed = IntegerField('מספר מיטה',validators=[DataRequired()])
    department = IntegerField('מספר מחלקה',validators=[DataRequired()])
    max_calls = IntegerField('מספר שיחות שבועיות',validators=[DataRequired()])


class ContactForm(FlaskForm):
    f_name = StringField('שם פרטי', validators=[DataRequired()])
    l_name = StringField('שם משפחה', validators=[DataRequired()])
    phone = StringField('מספר טלפון', validators=[DataRequired()])
    mail = StringField('כתובת מייל', validators=[DataRequired()])
    priority = IntegerField('עדיפות', validators=[DataRequired()])
    day = DateField(id='datepick')

class ContactTimeForm(FlaskForm):
    day = IntegerField('patient_id', validators=[DataRequired()])
    _from = TimeField('from', validators=[DataRequired()],choices=[utils.get_times_list()])
    to = TimeField('to', validators=[DataRequired()])