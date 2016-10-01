from sqlalchemy import Integer, String, Column, DateTime
from first_blog.database import Base
from datetime import datetime

class Blog(Base):
	__tablename__ = 'blog'
	id = Column(Integer, primary_key=True)	
	title = Column(String(101), nullable=False)
	content = Column(String(150), nullable=False)
	pub_date = Column(DateTime, nullable=False) 

	def __init__(self, title, content, pub_date=datetime.now()):
		self.title = title
		self.content = content
		self.pub_date = pub_date

	def __repr(self):
		return '<Blog %r>'%self.title
