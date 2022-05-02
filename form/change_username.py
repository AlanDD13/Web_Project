from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class ChangeUsernameForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('New Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
