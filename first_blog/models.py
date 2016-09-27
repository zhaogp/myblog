from sqlalchemy import Column, Integer, String
from first_blog.database import Base

class Blog(Base):
	__tablename__ = 'blog'
	id = Column(Integer, primary_key=True)	
	title = Column(String(100), nullable=False)
	content = Column(String(200), nullable=False)

	def __init__(self, title, content):
		self.title = title
		self.content = content

	
