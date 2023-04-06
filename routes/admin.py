import os
import csv
from app import app
from flask import render_template, request, redirect, url_for, abort, send_file
from flask_login import login_required, current_user
from models import *
from forms import *

#------------------------------------------------------------------------------------
# routes for admin (venue, event, user)
#------------------------------------------------------------------------------------

@app.route('/admin')
@login_required
def admin():
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    return render_template('admin.html', venues=Venue.query.all(), admin="admin")


@app.route('/admin/analytics')
@login_required
def analytics():
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    venues = Venue.query.all()
    shows = Show.query.all()
    bookings = Booking.query.all()
    users = User.query.all()
    venuenames = [venue.name for venue in venues]
    shownames = [show.name for show in shows]
    usernames = [user.name for user in users]
    showspervenue = [len(venue.shows) for venue in venues]
    bookingspershow = [len(show.bookings) for show in shows]
    bookingspervenue = [ sum([len(show.bookings) for show in venue.shows]) for venue in venues]
    bookingsperuser = [len(user.bookings) for user in users]
    kwargs = {
        'venues': venues,
        'shows': shows,
        'bookings': bookings,
        'venuenames': venuenames,
        'shownames': shownames,
        'usernames': usernames,
        'showspervenue': showspervenue,
        'bookingspershow': bookingspershow,
        'bookingspervenue': bookingspervenue,
        'bookingsperuser': bookingsperuser,
    }
    return render_template('analytics.html', **kwargs)


@app.route('/admin/export')
@login_required
def export():
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    venues = Venue.query.all()
    shows = Show.query.all()
    bookings = Booking.query.all()
    users = User.query.all()

    # if csv folder does not exist, create it
    if not os.path.exists(app.config['CSV_FOLDER']):
        os.makedirs(app.config['CSV_FOLDER'])
    else:
        # remove earlier zip files
        for file in os.listdir(app.config['CSV_FOLDER']):
            if file.endswith('.zip'):
                os.remove(os.path.join(app.config['CSV_FOLDER'], file))
    
    # if csv files already exist, delete them
    filenames = ['venues.csv', 'shows.csv', 'bookings.csv', 'users.csv']
    
    # create csv files for each table
    with open(os.path.join(app.config['CSV_FOLDER'], 'venues.csv'), 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['id', 'name', 'address', 'city', 'capacity'])
        for venue in venues:
            csvwriter.writerow([venue.id, venue.name, venue.address, venue.city, venue.capacity])
        
    with open(os.path.join(app.config['CSV_FOLDER'], 'shows.csv'), 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['id', 'venue_id', 'name', 'rating', 'start_time', 'end_time', 'price', 'tags'])
        for show in shows:
            csvwriter.writerow([show.id, show.venue_id, show.name, show.rating, show.start_time, show.end_time, show.price, show.tags])
    
    with open(os.path.join(app.config['CSV_FOLDER'], 'bookings.csv'), 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['id', 'show_id', 'user_id', 'booking_time', 'seats'])
        for booking in bookings:
            csvwriter.writerow([booking.id, booking.show_id, booking.user_id, booking.booking_time, booking.seats])

    
    with open(os.path.join(app.config['CSV_FOLDER'], 'users.csv'), 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['id', 'username', 'name', 'is_admin'])
        for user in users:
            csvwriter.writerow([user.id, user.username, user.name, user.is_admin])
    
    # zip the files and return the zip file
    import zipfile
    zipfilename = f'csv_{datetime.now().strftime("%Y%m%d%H%M%S")}.zip'
    zipfilepath = os.path.join(app.config['CSV_FOLDER'], zipfilename)
    with zipfile.ZipFile(zipfilepath, 'w') as zip:
        for filename in filenames:
            path = os.path.join(app.config['CSV_FOLDER'], filename)
            zip.write(path, arcname=filename)
            os.remove(path)

    return send_file(zipfilepath, as_attachment=True)
    