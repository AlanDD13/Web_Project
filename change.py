from flask import Blueprint, render_template, redirect
from flask_login import login_required
from form.change_password import ChangePasswordForm
from form.change_username import ChangeUsernameForm
from form.change_email import ChangeEmailForm
from data import db_session
from data.users import User


change = Blueprint('change', __name__, static_folder='static', template_folder='templates')


@change.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.new_password.data == form.new_password_submit.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.new_password.data):
                return render_template('change_password.html',
                                       message="Password shouldn't be same as old",
                                       form=form)
            else:
                user.set_password(form.new_password.data)
                db_sess.commit()
                return redirect('/')
        else:
            return render_template('change_password.html',
                                   message="Passwords are different",
                                   form=form)
    return render_template('change_password.html', form=form)


@change.route('/account/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            user.set_new_username(form.name.data)
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('change_username.html',
                                   message="Password doesn't fit",
                                   form=form)
    return render_template('change_username.html',form=form)


@change.route('/account/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        exists = db_sess.query(User.id).filter(User.email == form.new_email.data).first() is not None
        if exists:
            return render_template('change_email.html',
                                message="User with this email already exists",
                                form=form)
        else:
            if user and user.check_password(form.password.data):
                user.set_new_email(form.new_email.data)
                db_sess.commit()
                return redirect('/')
            else:
                return render_template('change_email.html',
                                   message="Password doesn't fit",
                                   form=form)
    return render_template('change_email.html', form=form)