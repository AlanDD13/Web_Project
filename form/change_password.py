from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password_submit = PasswordField('Submit New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
