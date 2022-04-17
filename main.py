from flask import Flask, render_template
from flask_login import login_required, LoginManager
from data import db_session
from change import change
from data.users import User
from authorization import authorization


app = Flask(__name__)
app.config['SECRET_KEY'] = 'laksjflaksjf'
app.register_blueprint(change)
app.register_blueprint(authorization)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/about_Kripto')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run('127.0.0.1', 8080)
