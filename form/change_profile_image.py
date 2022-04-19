from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ChangeProfileImage(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    submit = SubmitField('Submit')
