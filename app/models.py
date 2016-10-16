from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from app.database import Base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from . import login_manager

class Blog(Base):
	__tablename__ = 'blog'
	id = Column(Integer, primary_key=True)	
	title = Column(String(101), nullable=False)
	content = Column(String(150), nullable=False)
	pub_date = Column(DateTime, index=True) 

	def __init__(self, title, content, pub_date=datetime.now()):
		self.title = title
		self.content = content
		self.pub_date = pub_date

	def __repr__(self):
		return '<Blog %r>'%self.title

class User(UserMixin, Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(60), nullable=False)
	password_hash = Column(String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readalbe attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>'%self.username

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

