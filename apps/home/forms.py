from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TimeField, DateField, SelectField
from wtforms.validators import Email, DataRequired


class DepartmentTimesForm(FlaskForm):
    day = SelectField('יום', choices=[], validators=[DataRequired()])
    from_hour = SelectField('החל משעה', choices=[], validators=[DataRequired()])
    to_hour = SelectField('עד לשעה', choices=[], validators=[DataRequired()])


