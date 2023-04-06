from app import app
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import *
from forms import *
from error import flash_form_errors

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
