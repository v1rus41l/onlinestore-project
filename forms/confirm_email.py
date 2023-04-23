from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class ConfirmForm(FlaskForm):
    cod = StringField('Код', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')