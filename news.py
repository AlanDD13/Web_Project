import sqlite3
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from data import db_session
from data.users import User

news = Blueprint('news', __name__, static_folder='static', template_folder='templates')


def user_data(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    return user.image_file, user.username


@news.route('/<int:id>/<title>', methods=['GET'])
def news_page(id, title):
    # news data opening 
    con = sqlite3.connect("db/news.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM news WHERE id = {id}""").fetchall()
    news = {
        'news': [
            {
                "id": item[0],
                "title": item[1],
                "pre_content": item[2],
                "image": item[3],
                "content": item[4],
                
            }
            for item in result
        ]
    }
    con.close()
    # comments to these news
    con = sqlite3.connect("db/comments.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM comments WHERE news_id = {id}""").fetchall()
    comments = {
        'comments': [
            {
                'user_id': comment[1],
                'user_img': user_data(comment[1])[0],
                'user_username': user_data(comment[1])[1],
                'comment': comment[2],
                'date': comment[4]
            }
            for comment in result
        ]
    }
    con.commit()

    return render_template('news.html', id=id, title=title, news=news, comments=comments)


@news.route('/<int:id>/<title>', methods=['POST'])
def news_page_post(id, title):
    con = sqlite3.connect("db/comments.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO comments(user_id, comment, news_id, date) VALUES({current_user.id}, '{request.form['comment']}', {id}, '{datetime.now():%Y-%m-%d}')""")
    con.commit()

    return redirect(url_for('news.news_page', id=id, title=title))
