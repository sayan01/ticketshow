from flask_wtf import *
from wtforms import *
from wtforms.fields import *
from wtforms.validators import *
from wtforms.widgets import *
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class UpdateProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])

class ChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
class VenueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])

class ShowForm(FlaskForm):
    name = StringField('Name of Show', validators=[DataRequired(message="Name of Show is required"), Length(min=2, max=50)])
    rating = SelectField('Rating', validators=[DataRequired(message="Rating is required")], choices=[1,2,3,4,5], coerce=int)
    date = DateField('Date', validators=[DataRequired(message="Date is required")], default=date.today())
    start_time = TimeField('Start Time', validators=[DataRequired(message="Start Time is required")], format='%H:%M')
    end_time = TimeField('End Time', validators=[DataRequired(message="End Time is required")], format='%H:%M')
    tags = StringField('Tags', validators=[DataRequired(), Length(min=2, max=255)])
    ticket_price = DecimalField('Ticket Price', validators=[DataRequired()])
    venue = SelectField('Venue', coerce=int, validators=[DataRequired()])


class BookingForm(FlaskForm):
    seats = IntegerField('No. of Seats', validators=[DataRequired(), NumberRange(min=1)])


class VenueSearchForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])

class ShowSearchForm(FlaskForm):
    tags = StringField('Tags', validators=[DataRequired(), Length(min=2, max=50)])
    rating = SelectField('Rating', validators=[DataRequired()], choices=[1,2,3,4,5], coerce=int)
