from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import app
from models import *
from forms import *
from error import flash_form_errors
from datetime import datetime

#------------------------------------------------------------------------------------
# routes for user
#------------------------------------------------------------------------------------

@app.route('/' , methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('admin'))
    form = SearchForm()
    if form.validate_on_submit():
        venues = Venue.query.filter(Venue.city.ilike(f'%{form.location.data}%')).all() if form.location.data else Venue.query.all()
        kwargs = {
            'user': current_user,
            'venues': venues,
            'now': datetime.now(),
            'tags': [tag.strip() for tag in form.tags.data.split(',')] if form.tags.data else None,
            'rating': form.rating.data if form.rating.data else None,
            'location': form.location.data if form.location.data else None,
            'form': form,
        }
        return render_template('index.html', **kwargs)
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('index.html', user=current_user, venues=Venue.query.all(), now=datetime.now(), form=form)

@app.route('/show/<int:show_id>/book', methods=['GET', 'POST'])
@login_required
def book_show(show_id: int):
    show = Show.query.get_or_404(show_id)
    form = BookingForm()
    if form.validate_on_submit():
        # check if seats are available
        if form.seats.data < 0:
            flash('Seats cannot be negative')
            return redirect(url_for('book_show', show_id=show_id))
        if form.seats.data > show.venue.capacity - sum([booking.seats for booking in show.bookings]):
            flash('Not enough seats available')
            return redirect(url_for('book_show', show_id=show_id))
        # check if user has already booked
        booking = Booking.query.filter_by(user=current_user, show=show).first()
        if booking:
            flash('You have already booked this show, adding seats to your booking')
            booking.seats += form.seats.data
        else:
            # create booking
            booking = Booking( user=current_user, show=show, seats=form.seats.data)
            db.session.add(booking)
        db.session.commit()
        flash('Booking successful')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.seats.data = 1
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('show/book.html', form=form, show=show)

@app.route('/show/<int:show_id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel_show(show_id: int):
    show = Show.query.get_or_404(show_id)
    booking = Booking.query.filter_by(user=current_user, show=show).first_or_404()
    if booking.show.end_time < datetime.now():
        flash('Cannot cancel booking for a show that has already ended')
        return redirect(url_for('bookings'))
    if request.method == 'POST':
        db.session.delete(booking)
        db.session.commit()
        flash('Booking cancelled')
        return redirect(url_for('index'))
    return render_template('show/cancel.html', show=show, booking=booking)

@app.route('/bookings')
@login_required
def bookings():
    return render_template('bookings.html', user=current_user, now=datetime.now())