from flask import render_template, session, redirect, url_for
from datetime import datetime

from . import main
from ..database import db_session

@main.route('/', methods=['GET', 'POST'])
def index():
	cur = db_session.execute('select * from blog order by id desc')
	blogs = cur.fetchall()
	return render_template('main/index.html', entries=blogs)

