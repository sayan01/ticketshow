from flask import *
from flask_login import current_user, login_required, login_user, logout_user
from models import *
from forms import *
from error import flash_form_errors
from datetime import timedelta
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app import app

#------------------------------------------------------------------------------------
# routes for authentication
#------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # if no admin user exists, redirect to admin register page
    if not User.query.filter_by(is_admin=True).first():
        flash('No admin user exists. Please create one first.')
        return redirect(url_for('admin_register'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if User.query.filter_by(is_admin=True).first() and current_user.is_authenticated and not current_user.is_admin: # if admin user exists and current user is not admin, return 403
        abort(403, description="Access denied, you are not an admin")
    # if admin user exists, and currently not logged in, redirect to login page
    if User.query.filter_by(is_admin=True).first() and not current_user.is_authenticated:
        flash('Please login first')
        return redirect(url_for('login'))
    # if admin user does not exist, or current user is admin, allow admin register
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('admin_register'))
        user = User(username=form.username.data, name=form.name.data, is_admin=True)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Admin user created successfully')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('register.html', form=form, usertype='Admin')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=form.username.data, name=form.name.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('register.html', form=form, usertype='User')

#------------------------------------------------------------------------------------
# routes for admin
#------------------------------------------------------------------------------------

@app.route('/admin')
@login_required
def admin():
    # if logged in user is not admin, return 403
    if not current_user.is_admin:
        abort(403, description="Access denied, you are not an admin")
    return render_template('admin.html', venues=Venue.query.all())

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
    return render_template('venue/add.html', form=form)

#------------------------------------------------------------------------------------
# routes for user
#------------------------------------------------------------------------------------

@app.route('/')
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('admin'))
    return render_template('index.html')
        

#------------------------------------------------------------------------------------
# common routes
#------------------------------------------------------------------------------------

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = RegisterForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('edit_profile.html', form=form)


# Error pages ------------------------------------------------------------------------------------
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template('error.html', 
                           error_code=404, 
                           error_title='Page not found', 
                           error_message='The page you are looking for does not exist.<br><strong>'+e.description+'</strong>'
                        ), 404

# forbidden
@app.errorhandler(403)
def error403(e):
    return render_template('error.html',
                           error_code=403,
                           error_title='Access denied',
                           error_message='You do not have permission to access this page.<br><strong>'+e.description+'</strong><br><a href="'+url_for('login')+'">Login</a> with correct credentials to access this page.'
                        ), 403
    
# internal error
@app.errorhandler(500)
def error500(e):
    return render_template('error.html', 
                           error_code=500, 
                           error_title='Internal server error', 
                           error_message='An internal server error has occurred.<br><strong>'+e.description+'</strong><br>Try again later'
                        ), 500