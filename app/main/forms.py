from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Required


class BlogForm(FlaskForm):
	title = StringField('blog title', validators=[Required()])
	content = TextAreaField('what is your mind', validators=[Required()])
	submit = SubmitField('Submit')
