from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from form.user import RegisterForm
from form.login import LoginForm
from form.change_password import ChangePasswordForm
from data import db_session
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'laksjflaksjf'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="This User already exists")
        user = User(
            username=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/account/change_password', methods=['GET', 'POST'])
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
                User.set_password(form.new_password.data)
                db_sess.commit()
                return redirect('/')
        else:
            return render_template('change_password.html',
                                   message="Passwords are different",
                                   form=form)
    return render_template('change_password.html', form=form)


@app.route('/account/change_username')
@login_required
def change_username():
    return render_template('change_username.html')


@app.route('/account/change_email')
@login_required
def change_email():
    return render_template('change_email.html')


@app.route('/about_Kripto')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run('127.0.0.1', 8080)
