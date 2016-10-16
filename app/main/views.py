from flask import render_template, session, redirect, url_for
from datetime import datetime

from . import main
from ..database import db_session

@main.route('/', methods=['GET', 'POST'])
def index():
	cur = db_session.execute('select * from blog order by id desc')
	blogs = cur.fetchall()
	return render_template('main/index.html', entries=blogs)

@main.route('/add', methods=['GET', 'POST'])
def add():
	db_session.execute('insert into blog(title, content, pub_date) values("%s", "%s", "%s")'
		%(request.form['title'], request.form['content'], datetime.now()))	
	db_session.commit()
	flash('add a new blog')
	return redirect(url_for('index'))
