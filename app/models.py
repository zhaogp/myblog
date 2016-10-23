from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean
from app.database import Base, db_session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager

class Blog(Base):
	__tablename__ = 'blog'
	id = Column(Integer, primary_key=True)	
	title = Column(String(101), nullable=False)
	content = Column(String(150), nullable=False)
	pub_date = Column(DateTime, index=True) 
	author_id = Column(Integer, ForeignKey('user.id'))

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
	role_id = ForeignKey('role.id')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role_id == None:
			self.role_id = Role.query.filter_by(default=True).first()

	@property
	def password(self):
		raise AttributeError('password is not a readalbe attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def can(self, permission):
		return self.role_id is not None and \
			(self.role_id.permission & permission) == permission

	def __repr__(self):
		return '<User %r>'%self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permission):
		return False
	
	def is_administration(self):
		return False

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Role(Base):
	__tablename__ = 'role'
	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True)
	permission = Column(Integer)

	@staticmethod
	def insert_role():
		roles = {
			'User' : Permission.WRITE,
			'Admin' : Permission.ADMIN
		}
		
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permission = roles[r]
			db_session.add(role)
		
		db_session.commit()

	def __repr__(self):
		return '<Role %r>'%self.name

class Permission:
	WRITE = 0x04
	ADMIN = 0x80
