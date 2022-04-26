from flask import Blueprint, redirect, render_template, url_for, request
import sqlite3

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
                'comment': comment[2]
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
    cur.execute(f"""INSERT INTO comments(user_id, comment, news_id) VALUES({current_user.id}, '{request.form['comment']}', {id})""")
    con.commit()

    return redirect(url_for('news.news_page', id=id, title=title))