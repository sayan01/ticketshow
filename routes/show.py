from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from models import *
from forms import *
from error import flash_form_errors

# shows  ---------------------------------------------------------------------------


@app.route('/admin/show/add/<int:venue_id>', methods=['GET', 'POST'])
@login_required
def add_show(venue_id: int):
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    form = ShowForm()
    form.venue.choices = [(venue.id, venue.name)
                          for venue in Venue.query.all()]
    if form.validate_on_submit():
        venue = Venue.query.get_or_404(form.venue.data)
        date = form.date.data
        start_time = datetime.combine(date, form.start_time.data)
        end_time = datetime.combine(date, form.end_time.data)
        # check if start time is before end time
        if start_time >= end_time:
            flash('Start time must be before end time')
            return redirect(url_for('add_show', venue_id=venue_id))
        # check if start time is in the past
        if start_time < datetime.now():
            flash('Start time cannot be in the past')
            return redirect(url_for('add_show', venue_id=venue_id))

        # check if show already exists at this time
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time <= start_time, Show.end_time >= start_time).first():
            flash('Show already exists at this time')
            return redirect(url_for('add_show', venue_id=venue_id))
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time <= end_time, Show.end_time >= end_time).first():
            flash('Show already exists at this time')
            return redirect(url_for('add_show', venue_id=venue_id))
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time >= start_time, Show.end_time <= end_time).first():
            flash('Show already exists at this time')
            return redirect(url_for('add_show', venue_id=venue_id))
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time <= start_time, Show.end_time >= end_time).first():
            flash('Show already exists at this time')
            return redirect(url_for('add_show', venue_id=venue_id))
        if form.ticket_price.data < 0:
            flash('Ticket price cannot be negative')
            return redirect(url_for('add_show', venue_id=venue_id))

        show = Show(venue=venue, name=form.name.data, start_time=start_time, end_time=end_time,
                    price=form.ticket_price.data, rating=form.rating.data, tags=",".join(
                        [token.lower().strip() for token in form.tags.data.strip().split(',')])
                    )
        db.session.add(show)
        db.session.commit()
        flash('Show added successfully')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        if venue_id:
            form.venue.data = venue_id

    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('show/add.html', form=form, form_fields_readonly=False)

@app.route('/admin/show/<int:show_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_show(show_id: int):
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    form = ShowForm()
    form.venue.choices = [(venue.id, venue.name)
                          for venue in Venue.query.all()]
    show = Show.query.get_or_404(show_id)
    if form.validate_on_submit():
        venue = Venue.query.get_or_404(form.venue.data)
        date = form.date.data
        start_time = datetime.combine(date, form.start_time.data)
        end_time = datetime.combine(date, form.end_time.data)
        # check if start time is before end time
        if start_time >= end_time:
            flash('Start time must be before end time')
            return redirect(url_for('edit_show', show_id=show_id))
        # check if start time is in the past
        # if start_time < datetime.now():
        #     flash('Start time cannot be in the past')
        #     return redirect(url_for('edit_show', show_id=show_id))

        # check if show already exists at this time which is not the current show
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time <= start_time, Show.end_time >= start_time).filter(Show.id != show.id).first():
            flash('Show already exists at this time')
            return redirect(url_for('edit_show', show_id=show_id))
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time <= end_time, Show.end_time >= end_time).filter(Show.id != show.id).first():
            flash('Show already exists at this time')
            return redirect(url_for('edit_show', show_id=show_id))
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time >= start_time, Show.end_time <= end_time).filter(Show.id != show.id).first():
            flash('Show already exists at this time')
            return redirect(url_for('edit_show', show_id=show_id))
        if Show.query.filter_by(venue_id=venue.id).filter(
                Show.start_time <= start_time, Show.end_time >= end_time).filter(Show.id != show.id).first():
            flash('Show already exists at this time')
            return redirect(url_for('edit_show', show_id=show_id))
        if form.ticket_price.data < 0:
            flash('Ticket price cannot be negative')
            return redirect(url_for('edit_show', show_id=show_id))

        show.venue = venue
        show.name = form.name.data
        show.start_time = start_time
        show.end_time = end_time
        show.price = form.ticket_price.data
        show.rating = form.rating.data
        show.tags = form.tags.data
        db.session.commit()
        flash('Show updated successfully')
        return redirect(url_for('admin'))
    if request.method == 'GET':
        form.venue.data = show.venue_id
        form.name.data = show.name
        form.date.data = show.start_time.date()
        form.start_time.data = show.start_time.time()
        form.end_time.data = show.end_time.time()
        form.ticket_price.data = show.price
        form.rating.data = show.rating
        form.tags.data = show.tags
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('show/edit.html', form=form, form_fields_readonly=False)

@app.route('/admin/show/<int:show_id>/delete', methods=['GET', 'POST'])
def delete_show(show_id: int):
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    show = Show.query.get_or_404(show_id)
    form = ShowForm()
    form.venue.choices = [(show.venue.id, show.venue.name)]
    if form.validate_on_submit():
        db.session.delete(show)
        db.session.commit()
        flash('Show deleted successfully')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.venue.data = show.venue_id
        form.name.data = show.name
        form.start_time.data = show.start_time
        form.end_time.data = show.end_time
        form.ticket_price.data = show.price
        form.rating.data = show.rating
        form.tags.data = show.tags
    return render_template('show/delete.html', form=form, show=show, form_fields_readonly=True)