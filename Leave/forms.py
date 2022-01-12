from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired


class Addworkform(FlaskForm):
    workname = StringField(label='Your work:', validators=[Length(min=2, max=99), DataRequired()])
    workdetail = TextAreaField(label='Work detail:', validators=[DataRequired()])
    workplace = StringField(label='Place:', validators=[Length(min=2, max=99), DataRequired()])
    workdate = DateField(label='Date:', validators=[DataRequired()])
    submit = SubmitField(label='Create your job')