from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])


class VenueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])


class ShowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    rating = DecimalField('Rating', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired(), Length(min=2, max=50)])
    ticket_price = DecimalField('Ticket Price', validators=[DataRequired()])
    venue = SelectField('Venue', coerce=int, validators=[DataRequired()])


class BookingForm(FlaskForm):
    show = SelectField('Show', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=date.today())
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class VenueSearchForm(FlaskForm):
    location = SelectField('Location', validators=[DataRequired()], choices=[], coerce=int)

class ShowSearchForm(FlaskForm):
    tags = SelectField('Tags', validators=[DataRequired()], choices=[], coerce=int)
    rating = SelectField('Rating', validators=[DataRequired()], choices=[], coerce=int)
