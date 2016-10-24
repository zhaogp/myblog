from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, EqualTo, Regexp

from app.models import User
from app.database import db_session


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('keep me login')
	submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[Required(),
		Length(2, 64), Regexp('^[a-zA-Z][A-Za-z0-9_]*$', 0,
		'username must have only letters, numbers or underscores')])
	password = PasswordField('Password', validators=[Required(),
		EqualTo('password2', message='input password must match')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('submit')

	def validate_username(self, field):
		if db_session.query(User).filter_by(username=field.data).first():
			raise ValidationError('Username already in use')
