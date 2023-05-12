from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user
from app import app
from models import *
from forms import *
from error import flash_form_errors
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
    return render_template('auth/login.html', form=form)

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
    return render_template('auth/register.html', form=form, usertype='Admin')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if no admin user exists, redirect to admin register page
    if not User.query.filter_by(is_admin=True).first():
        flash('No admin user exists. Please create one first.')
        return redirect(url_for('admin_register'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        # password should have 1 small, 1u upper case, 1 symbol, 1 number
        hasLower = False
        hasUpper = False
        hasNumber = False
        hasSymbol = False
        from string import ascii_lowercase, ascii_uppercase, digits
        for char in form.password.data:
            if char in ascii_uppercase:
                hasUpper = True
            if char in ascii_lowercase:
                hasLower = True
            if char in digits:
                hasNumber = True
            if char in "!@#$%^&*()_+{}:>?<\"":
                hasSymbol = True
        if not (hasLower and hasUpper and hasNumber and hasSymbol):
            flash("Password needs to contain atleast 1 uppercase, 1 lowercase, 1 number, and 1 symbol")
            return redirect(url_for('register'))
        user = User(username=form.username.data, name=form.name.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('auth/register.html', form=form, usertype='User')
