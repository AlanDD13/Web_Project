import os
import secrets

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from PIL import Image

from data import db_session
from data.users import User
from errors import check_password
from form.change_email import ChangeEmailForm
from form.change_password import ChangePasswordForm
from form.change_profile_image import ChangeProfileImage
from form.change_username import ChangeUsernameForm

change = Blueprint('change', __name__, static_folder='static', template_folder='templates')


@change.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.new_password.data == form.new_password_submit.data:
            if current_user.email == form.email.data:
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.email == form.email.data).first()
                if user and user.check_password(form.password.data):
                    if user and user.check_password(form.new_password.data):
                        return render_template('change_password.html',
                                            message="Password shouldn't be same as old",
                                            form=form)
                    else:
                        try:
                            if check_password(str(form.password.data)):
                                user.set_password(form.new_password.data)
                                db_sess.commit()
                                return redirect('/')
                        except Exception as error:
                            return render_template('change_password.html', title='change password',
                                        form=form,
                                        message=error.message)
                else:
                    return render_template('change_password.html', title='change password',
                                        form=form,
                                        message="Old Password doesn't fit")
            else:
                return render_template('change_password.html', title='change password',
                                        form=form,
                                        message="Use your own email")
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
        if current_user.email == form.email.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if db_sess.query(User).filter(User.username == form.name.data).first():
                    return render_template('change_username.html', title='change username',
                                    form=form,
                                    message="User with such username already exists")
            if user and user.check_password(form.password.data):
                user.set_new_username(form.name.data)
                db_sess.commit()
                return redirect('/')
            else:
                return render_template('change_username.html',
                                    message="Password doesn't fit",
                                    form=form)
        else:
            return render_template('change_username.html',
                                    message="Use your own email",
                                    form=form)
    return render_template('change_username.html',form=form)


@change.route('/account/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.email == form.email.data:
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
        else:
            return render_template('change_username.html',
                                    message="Use your own email",
                                    form=form)
    return render_template('change_email.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(change.root_path, 'static/img/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@change.route('/account/change_profile_picture', methods=['GET', 'POST'])
@login_required
def change_profile_picture():
    form = ChangeProfileImage()
    if form.validate_on_submit():
        if form.picture.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == current_user.email).first()
            picture_file = save_picture(form.picture.data)
            if user.image_file == 'static/img/profile_pics/default.png':
                user.image_file = f'static/img/profile_pics/{picture_file}'
                db_sess.commit()
                return redirect('/')
            else:
                os.remove(os.path.join(change.root_path, user.image_file))
                user.image_file = f'static/img/profile_pics/{picture_file}'
                db_sess.commit()
                return redirect('/')
    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)
    return render_template('change_profile_picture.html',
                           image_file=image_file, form=form)
