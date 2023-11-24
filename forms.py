from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, ValidationError
from wtforms.validators import DataRequired, URL, NumberRange, Optional
from flask_wtf.csrf import CSRFProtect

url_validator = URL()


class RegisterUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])


class LoginUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class Feedback_form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Feedback", validators=[DataRequired()])
