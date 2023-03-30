from flask_wtf import *
from wtforms import *
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

class VenueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])


class ShowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    rating = SelectField('Rating', validators=[DataRequired()], choices=[1,2,3,4,5], coerce=int)
    tags = StringField('Tags', validators=[DataRequired(), Length(min=2, max=50)])
    ticket_price = DecimalField('Ticket Price', validators=[DataRequired()])
    venue = SelectField('Venue', coerce=int, validators=[DataRequired()])


class BookingForm(FlaskForm):
    show = SelectField('Show', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=date.today())
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class VenueSearchForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])

class ShowSearchForm(FlaskForm):
    tags = StringField('Tags', validators=[DataRequired(), Length(min=2, max=50)])
    rating = SelectField('Rating', validators=[DataRequired()], choices=[1,2,3,4,5], coerce=int)
