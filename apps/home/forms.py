from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired
import pandas as pd

def get_hours_list():
    a = pd.date_range("07:00", "18:00", freq="1H").strftime('%H:%M')
    hours = [(value, value) for value in a]
    return hours

def get_days_list():
    d = dict({
        "1": "ראשון",
        "2": "שני",
        "3": "שלישי",
        "4": "רביעי",
        "5": "חמישי",
        "6": "שישי",
        "7": "שבת"
    })
    return [(key, value) for (key, value) in d.items()]


class DepartmentTimesForm(FlaskForm):
    day = SelectField('יום', choices=get_days_list(), validators=[DataRequired()])
    from_hour = SelectField('החל משעה', choices=get_hours_list(), validators=[DataRequired()])
    to_hour = SelectField('עד לשעה', choices=get_hours_list(), validators=[DataRequired()])



