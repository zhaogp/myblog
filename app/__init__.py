from flask import Flask, render_template
from config import config
import click
from .database import db_session, init_db

def create_app(config_name='default'):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

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
