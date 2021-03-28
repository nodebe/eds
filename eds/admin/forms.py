from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError, Email

class FAQForm(FlaskForm):
	question = StringField('Question', validators=[DataRequired()])
	answer = TextAreaField('Answer', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(FAQForm, self).__init__(*args, **kwargs)


class NotificationForm(FlaskForm):
	title = StringField('', validators=[DataRequired(), Length(max=40)])
	message = TextAreaField('', validators=[DataRequired()])
	icon = StringField('')

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(NotificationForm, self).__init__(*args, **kwargs)
