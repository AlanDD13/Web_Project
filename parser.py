import sqlite3

import requests
from bs4 import BeautifulSoup

from errors import *

URL = 'https://cointelegraph.com/tags/bitcoin'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://cointelegraph.com/'


def news_content(url):
    html = get_html(url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find('div', class_='post-content')
        line = ''
        for item in items:
            line += str(item)

        return line
    else:
        raise ArticleConnectionError(f'Problems with connection to article: {html.status_code}')


def news_image(url):
    html = get_html(url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('div', class_='post-cover post__block post__block_cover')
        try:
            for item in items:
                image = item.find('picture').find('img').attrs['src']
            
            return image
        except Exception as e:
            return ''

    else:
        raise ArticleConnectionError(f'Problems with connection to article: {html.status_code}')


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='posts-listing__item')

    news = []
    for item in items:
        news.append({
            'title': item.find('span', class_='post-card-inline__title').get_text(strip=True),
            'img': news_image(HOST + item.find('a', class_='post-card-inline__title-link').get('href')),
            'pre_content' : item.find('p', class_='post-card-inline__text').get_text(strip=True),
            'content': news_content(HOST + item.find('a', class_='post-card-inline__title-link').get('href')),
            'date': item.find('div', class_='post-card-inline__meta').find_next('time').attrs['datetime']
        })
    return news


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        news = get_content(html.text)
        
        con = sqlite3.connect("db/news.db")
        cur = con.cursor()
        for item in news:
            if cur.execute(f"""SELECT * FROM news WHERE title = ?""", (str(item['title']), )).fetchall():
                continue
            else:
                cur.execute(f"""INSERT INTO news(title, pre_content, image, content, date) VALUES(?, ?, ?, ?, ?)""", (str(item['title']),\
                     str(item['pre_content']), str(item['img']), str(item['content']), str(item['date'])))
                con.commit()
    else:
        raise ArticleConnectionError(f'Problems with connection to website: {html.status_code}')
