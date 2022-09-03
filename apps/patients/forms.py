# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField
from wtforms.validators import Email, DataRequired

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
    contact_id = IntegerField('patient_id', validators=[DataRequired()])
    f_name = StringField('f_name', validators=[DataRequired()])
    l_name = StringField('l_name', validators=[DataRequired()])
    phone = StringField('l_name', validators=[DataRequired()])
    mail = StringField('l_name', validators=[DataRequired()])
    priority = IntegerField('l_name', validators=[DataRequired()])

class ContactTimeForm(FlaskForm):
    num = IntegerField('patient_id', validators=[DataRequired()])
    _from = TimeField('from', validators=[DataRequired()])
    to = TimeField('to', validators=[DataRequired()])


