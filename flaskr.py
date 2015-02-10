# -*- coding: utf-8 -*-
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from werkzeug.utils import secure_filename
from contextlib import closing
###########
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
#################
from models import *


class MyForm(Form):
    #name = TextField('name', validators=[DataRequired()])
    name = TextField(u'名称', validators=[DataRequired()])

UPLOAD_FOLDER = 'D:\\TryRoot\\flaskr\\static\\Uploads'
DATABASE = 'D:\\TryRoot\\flaskr\\flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#from flaskr import init_db
# init_db()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)  # 获取一个安全的文件名，且仅仅支持ascii字符；
        pathfilename = os.path.join(UPLOAD_FOLDER, fname)
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        # f.save('d:\\a.sql')

    return '上传成功'


@app.route('/mywtf', methods=['POST', 'GET'])
def mywtf():
    form = MyForm()
    if request.method == 'GET':
        return render_template('mywtf.html', f=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            return 'sumit is success , name is %s' % form.name.data
        else:
            return 'submit is fail'


@app.route('/')
def show_entries():
    #cur = g.db.execute('selct title,text from entries eorder by id desc')

    # s
    #     lucy = text(title='lucy', fulltitle='lucy.F', password='asdf')
    # s.add(lucy)
    # s.commit()

    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    s = DBSession()
    e = s.query(entries).all()

    return render_template('show_entries.html', entries=e)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    # g.db.execute('insert into entries (title, text) values(?,?)',
    #             [request.form['title'], request.form['text']])
    # g.db.commit()

    e = entries(title=request.form['title'], text=request.form['text'])
    s = DBSession()
    s.add(e)
    s.commit()
# s
#     text = [text(title='maven', fulltitle='maven.sms', password='1234'),
#             text(title='fang', fulltitle='zhang fang', password='lkjhsd')]
# s.add_all(text)
# s.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
