from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import app
from models import *
from forms import *
from error import flash_form_errors

#------------------------------------------------------------------------------------
# routes for user
#------------------------------------------------------------------------------------

@app.route('/')
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('admin'))
    return render_template('index.html')

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
        if form.seats.data > show.venue.capacity - len(show.bookings):
            flash('Not enough seats available')
            return redirect(url_for('book_show', show_id=show_id))
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
