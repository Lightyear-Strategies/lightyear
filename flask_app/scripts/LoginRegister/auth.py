from flask_app.scripts.create_flask_app import db, login_manager
from flask_app.scripts.LoginRegister.models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_app.scripts.forms import  RegistrationForm, LoginForm
from flask import render_template,flash,redirect, url_for, request


def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password1.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


def login():
    form = LoginForm()
    if form.validate_on_submit():
        if "@" in form.username_email.data:
            user = User.query.filter_by(email=form.username_email.data).first()
        else:
            user = User.query.filter_by(username=form.username_email.data).first()

        remember = True if request.form.get('remember') else False
        if user and not user.check_password(form.password.data):
            flash('Invalid password.')
            return redirect(url_for('login'))

        login_user(user,remember=remember)
        return redirect(url_for('welcome'))

    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))
