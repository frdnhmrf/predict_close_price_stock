from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DecimalField, StringField


class PredictForm(FlaskForm):
    date = StringField('Date')
    date1 = StringField('Date ke-1')
    date2 = StringField('Date ke-2')
    date3 = StringField('Date ke-3')
    date4 = StringField('Date ke-4')
    date5 = StringField('Date ke-5')
    open = DecimalField('Open')
    high = DecimalField('High')
    low = DecimalField('Low')
    adj_close = DecimalField('Adj Close')
    volume = IntegerField('Volume')
    submit = SubmitField('Predict')
    close = ""  # this variable is used to send information back to the front page
    close_date_1 = ""
    close_date_2 = ""
    close_date_3 = ""
    close_date_4 = ""
    close_date_5 = ""
