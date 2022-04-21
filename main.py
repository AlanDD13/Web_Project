from flask import Flask, render_template
from flask_login import LoginManager, login_required

from authorization import authorization
from change import change
from data import db_session
from data.users import User
import json
import sqlite3

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
    con = sqlite3.connect("db/news.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM news""").fetchall()
    news = {
        'news': [
            {
                "id": item[0],
                "title": item[1],
                "image": item[2],
                "content": ' '.join(item[3].split()[:100]) + '...'
            }
            for item in result
        ]
    }

    con.close()
    return render_template('index.html', news=news)


@app.route('/<int:id>/<title>')
def news(id, title):
    con = sqlite3.connect("db/news.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM news WHERE id = {id}""").fetchall()
    content = {}
    for item in result:
        for i in range(len(item[3].split('\\n'))):
            content[f"content{i}"] = item[3].split('\\n')[i] 
    news = {
        'news': [
            {
                "id": item[0],
                "title": item[1],
                "image": item[2],
                "content": content
                
            }
            for item in result
        ]
    }
    print(content)
    return render_template('news.html', news=news)


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
