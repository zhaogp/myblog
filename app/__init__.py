from flask import Flask, render_template
from config import config
import click
from .database import db_session, init_db
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name='default'):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	login_manager.init_app(app)
	bootstrap = Bootstrap(app)
	return app

# @app.teardown_appcontext
# def shutdown_session(exception=None):
	# db_session.remove()

@click.command()
def initdb_command():
	init_db()
	print('new init db ...')

@click.command()
def run_command():
	print('run app ...')
	app = create_app()
	app.run('0.0.0.0', 5005, True)
