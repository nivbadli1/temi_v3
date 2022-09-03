# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('מספר המחלקה',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('סיסמה',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('מספר המחלקה',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('כתובת דואר אלקטרוני',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('סיסמת התחברות',
                             id='pwd_create',
                             validators=[DataRequired()])
