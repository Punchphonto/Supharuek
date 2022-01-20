from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class Additemform(FlaskForm):
    item_name = StringField(label='Item Name:', validators=[Length(min=2, max=99), DataRequired()])
    item_code = StringField(label='Barcode:', validators=[DataRequired()])
    description = TextAreaField(label='Description:', validators=[DataRequired()])
    psc = IntegerField(label='Amount', validators=[NumberRange(min=1), DataRequired()])
 

