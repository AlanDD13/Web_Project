from flask import Blueprint, redirect, render_template
from flask_login import login_required, login_user, logout_user

from data import db_session
from data.users import User
from errors import check_password
from form.login import LoginForm
from form.user import RegisterForm

authorization = Blueprint('authorization', __name__, static_folder='static', template_folder='templates')


@authorization.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='registration',
                                   form=form,
                                   message="User with such email already exists")
        if db_sess.query(User).filter(User.username == form.name.data).first():
            return render_template('register.html', title='registration',
                                   form=form,
                                   message="User with such username already exists")
        try:
            if check_password(str(form.password.data)):
                user = User(
                    username=form.name.data,
                    email=form.email.data,
                )
                user.set_password(form.password.data)
                db_sess.add(user)
                db_sess.commit()
                return redirect('/login')
        except Exception as error:
            return render_template('register.html', title='registration',
                                   form=form,
                                   message=error.message)
    return render_template('register.html', title='registration', form=form)


@authorization.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong email or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@authorization.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
