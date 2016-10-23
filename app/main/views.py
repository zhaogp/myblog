from flask import render_template, session, redirect, url_for
from datetime import datetime
from flask_login import current_user

from . import main
from ..database import db_session
from flask_login import current_user
from app.main.forms import BlogForm


@main.route('/', methods=['GET', 'POST'])
def index():
	form = BlogForm()
	
	cur = db_session.execute('select * from blogs order by id desc')
	blogs = cur.fetchall()
	return render_template('main/index.html', entries=blogs)

