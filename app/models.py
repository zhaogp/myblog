from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean
from app.database import Base, db_session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from sqlalchemy.orm import relationship


class Blog(Base):
	__tablename__ = 'blogs'
	id = Column(Integer, primary_key=True)	
	title = Column(String(101), nullable=False)
	content = Column(String(150), nullable=False)
	pub_date = Column(DateTime, index=True) 
	author_id = Column(Integer, ForeignKey('users.id'))

	author = relationship('User', back_populates='blogs')

	def __init__(self, title, content, pub_date=datetime.now()):
		self.title = title
		self.content = content
		self.pub_date = pub_date

	def __repr__(self):
		return '<Blog %r>'%self.title

class User(UserMixin, Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String(50), nullable=False)
	password_hash = Column(String(100))
	role_id = Column(Integer, ForeignKey('roles.id'))

	role = relationship('Role', back_populates='users')
	blogs = relationship('Blog', back_populates='author')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)

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
		if permission == 'READ':
			return True
		return False
	
	def is_administration(self):
		return False

class Role(Base):
	__tablename__ = 'roles'
	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True)
	permission = Column(Integer)

	users = relationship('User', order_by=User.username, back_populates='role')

	@staticmethod
	def insert_role():
		roles = {
			'User' : (Permission.WRITE | Permission.READ),
			'Admin' : Permission.ADMIN,
			'Anonymous' : Permission.READ
		}
		
		for r in roles:
			role = db_session.query(Role).filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permission = roles[r]
			db_session.add(role)
		
		db_session.commit()

	def __repr__(self):
		return '<Role %r>'%self.name

class Permission:
	READ = 0x01
	WRITE = 0x04
	ADMIN = 0x80

@login_manager.user_loader
def load_user(user_id):
	return db_session.query(User).filter_by(id=user_id)

