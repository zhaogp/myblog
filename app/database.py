from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://admin:11111@localhost:3306/blog?charset=utf8',
							echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
	autoflush=False, bind=engine))

Base = declarative_base()

def init_db():
	import app.models
	Base.metadata.create_all(bind=engine)

