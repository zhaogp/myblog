from flask import Flask, g, url_for, render_template, request, redirect
import os
import click
import sqlite3

app = Flask(__name__)

#配置信息
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'myblog.db')
))

#库表信息
def conn_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = conn_db()
	return g.sqlite_db

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@click.command()
def initdb_command():
	init_db()
	print('init db ...')

@click.command()
def run_command():
	app.run('0.0.0.0', 5005, True)

@app.route('/')
def show_blogs():
	db = get_db()
	cur = db.execute('select title, content from blog order by id desc')
	blogs = cur.fetchall()
	return render_template('index.html', entries=blogs)

@app.route('/add')
def add_blog():
	db = get_db()
	db.execute('insert into blog(title, content) values(?, ?)', 
				[request.form['title'], request.form['content']])
	db.commit()
	flash('a new blog')
	return redirect(url_for('show_blogs'))
	
