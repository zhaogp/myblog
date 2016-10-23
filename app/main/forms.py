from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required


class BlogForm(FlaskForm):
	body = TextAreaField('what is your mind', validators=[Required()])
	submit = SubmitField('Submit')
