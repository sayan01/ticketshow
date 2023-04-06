from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import app
from models import *
from forms import *
from error import flash_form_errors

#------------------------------------------------------------------------------------
# common routes
#------------------------------------------------------------------------------------

@app.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html', user=current_user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('profile/edit_profile.html', user=current_user, form=form)


@app.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash('Password Changed successfully')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        pass
    elif request.method == 'POST':
        flash_form_errors(form)
    return render_template('profile/change_password.html', user=current_user, form=form)
