from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://admin:11111@169.254.0.100:3306/blog', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
	autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	import first_blog.models
	Base.metadata.create_all(bind=engine)

