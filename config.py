import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'flask'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
	USERNAME = 'admin'
	PASSWORD = '11111'

	@staticmethod
	def init_app(self):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
		or 'mysql://admin:11111@localhost:3306/blog?charset=utf8'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') \
		or 'mysql://admin:11111@localhost:3307/blog?charset=utf8'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
		or 'mysql://admin:11111@localhost:3308/blog?charset=utf8'

config = {
	'development' : DevelopmentConfig,
	'testing' : TestingConfig,
	'production' : ProductionConfig,
	
	'default' : DevelopmentConfig
}
