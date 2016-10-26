from flask import render_template, session, redirect, url_for
from datetime import datetime
from flask_login import current_user
from datetime import datetime

from . import main
from ..database import db_session
from app.main.forms import BlogForm
from app.models import Permission, Blog


@main.route('/', methods=['GET', 'POST'])
def index():
	form = BlogForm()
	if current_user.can(Permission.WRITE) and form.validate_on_submit():
		blog = Blog(title=form.title.data, content=form.content.data,
			author=current_user._get_current_object(), pub_date=datetime.now())
		db_session.add(blog)
		db_session.commit()
		return redirect(url_for('main.index'))
	blogs = db_session.query(Blog).order_by(Blog.pub_date.desc()).all()
	return render_template('main/index.html', form=form, blogs=blogs, Permission=Permission)
		
		

