# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import Email, DataRequired

# login and registration

class PatientForm(FlaskForm):
    patient_id = StringField('patient_id',validators=[DataRequired()])
    f_name = StringField('f_name',validators=[DataRequired()])
    l_name = StringField('l_name',validators=[DataRequired()])
    bed = IntegerField('bed',validators=[DataRequired()])
    department = IntegerField('department',validators=[DataRequired()])
    max_calls = IntegerField('max_calls',validators=[DataRequired()])

