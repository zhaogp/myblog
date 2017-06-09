from flask import Flask, g, url_for, render_template, request, redirect, session, flash
import os
import click
import sqlite3
from app.database import db_session, init_db
from datetime import datetime

app = Flask(__name__)

#配置信息
app.config.update(dict(
	USERNAME='admin',
	PASSWORD='admin',
	SECRET_KEY='key',
))


@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

#库表信息
def conn_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = conn_db()
	return g.sqlite_db

def initdb():
	with app.app_context():
		init_db()

@click.command()
def initdb_command():
	initdb()
	print('init db ...')

@click.command()
def run_command():
	app.run('0.0.0.0', 5005, True)

@app.route('/')
def show_blogs():
	cur = db_session.execute('select * from blogs order by id desc')
	blogs = cur.fetchall()
	return render_template('index.html', entries=blogs)

@app.route('/add', methods=['POST'])
def add_blog():
	db_session.execute('insert into blog(title, content, pub_date) values("%s", "%s", "%s")'
		%(request.form['title'], request.form['content'], datetime.now()))
	db_session.commit()
	flash('a new blog')
	return redirect(url_for('show_blogs'))
	
@app.route('/login', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['loginname'] != app.config['USERNAME']:
			error = 'invalid username'
		elif request.form['nloginpwd'] != app.config['PASSWORD']:
			error = 'invalid password'
		else:
			session['logged_in'] = True
			flash('i am login')
			return redirect(url_for('show_blogs'))
	return render_template('login.html', ierror=error)
			
@app.route('/logout')
def logout():	
	session.pop('logged_in', None)
	flash('is logged out')
	return redirect(url_for('show_blogs'))
