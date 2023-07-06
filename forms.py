from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DecimalField, StringField


class PredictForm(FlaskForm):
    date = StringField('Date')
    open = DecimalField('Open')
    high = DecimalField('High')
    low = DecimalField('Low')
    adj_close = DecimalField('Adj Close')
    volume = IntegerField('Volume')
    submit = SubmitField('Predict')
    close = ""  # this variable is used to send information back to the front page
