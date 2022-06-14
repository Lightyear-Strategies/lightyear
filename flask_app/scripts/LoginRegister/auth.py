from flask_app.scripts.create_flask_app import db, login_manager
from flask_app.scripts.LoginRegister.models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_app.scripts.forms import  RegistrationForm, LoginForm
from flask import render_template,flash,redirect, url_for


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
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('welcome'))
        else:
            flash('Invalid password.')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))
