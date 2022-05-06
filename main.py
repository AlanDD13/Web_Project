import sqlite3

from flask import Flask, render_template
from flask_login import LoginManager, login_required

from authorization import authorization
from change import change
from data import db_session
from data.users import User
from news import news

app = Flask(__name__)
app.config['SECRET_KEY'] = 'laksjflaksjf'
app.register_blueprint(change)
app.register_blueprint(authorization)
app.register_blueprint(news)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    con = sqlite3.connect("db/news.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM news""").fetchall()
    news = {
        'news': sorted([
            {
                "id": int(item[0]),
                "title": item[1],
                "image": item[3],
                "content": item[2],
                "date": item[5]
            }
            for item in result
        ], key=lambda x: x['id'], reverse=True)
    }

    con.close()
    return render_template('index.html', news=news)


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
