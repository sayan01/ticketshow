from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app import app
from models import *
from forms import *
from error import flash_form_errors

@app.route('/admin/venue/add', methods=['GET', 'POST'])
@login_required
def add_venue():
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, address=form.address.data, city=form.city.data.upper(), capacity=form.capacity.data)
        db.session.add(venue)
        db.session.commit()
        flash('Venue added successfully')
        return redirect(url_for('admin'))
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('venue/add.html', form=form, form_fields_readonly=False)

@app.route('/admin/venue/<int:venue_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_venue(venue_id: int):
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm()
    if form.validate_on_submit():
        venue.name = form.name.data
        venue.address = form.address.data
        venue.city = form.city.data.upper()
        venue.capacity = form.capacity.data
        db.session.commit()
        flash('Venue updated successfully')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.name.data = venue.name
        form.address.data = venue.address
        form.city.data = venue.city
        form.capacity.data = venue.capacity
    return render_template('venue/edit.html', form=form, venue=venue, form_fields_readonly=False)

@app.route('/admin/venue/<int:venue_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_venue(venue_id: int):
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)
    if request.method == 'POST':
        for show in venue.shows:
            for booking in show.bookings:
                db.session.delete(booking)
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue deleted successfully')
        return redirect(url_for('admin'))
    else:
        form.name.data = venue.name
        form.address.data = venue.address
        form.city.data = venue.city
        form.capacity.data = venue.capacity
        return render_template('venue/delete.html', venue=venue, form=form, form_fields_readonly=True)
