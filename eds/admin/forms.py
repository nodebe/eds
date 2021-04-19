from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from eds.models import Department, Grade, Employee

def department_query():
	return Department.query

def grade_query():
	return Grade.query

def employee_query():
	return Employee.query

class AdminRegForm(FlaskForm):
	username = StringField('', validators=[DataRequired()])
	email = StringField('', validators=[DataRequired()])
	password = PasswordField('', validators=[DataRequired('Please choose a strong password'), Length(min=6)])
	confirm = PasswordField('', validators=[EqualTo('password')])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(AdminRegForm, self).__init__(*args, **kwargs)

class AdminLogForm(FlaskForm):
	email = StringField('', validators=[DataRequired('Please fill in a your email address')])
	password = PasswordField('', validators=[DataRequired('Please fill in your password'), Length(min=6)])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(AdminLogForm, self).__init__(*args, **kwargs)

class NewEmployeeForm(FlaskForm):
	firstname = StringField('', validators=[DataRequired()])
	lastname = StringField('', validators=[DataRequired()])
	dob = DateField('', validators=[DataRequired()])
	doj = DateField('', validators=[DataRequired()])
	address = StringField('', validators=[DataRequired()])
	city = StringField('', validators=[DataRequired()])
	state = StringField('', validators=[DataRequired()])
	phone = StringField('', validators=[DataRequired()])
	nin = StringField('', validators=[DataRequired()])
	id_card = FileField('', validators=[FileAllowed(['jpg','png', 'jpeg','JPG','JPEG','PNG'])])
	email = StringField('', validators=[DataRequired()])
	department = QuerySelectField(query_factory=department_query, allow_blank=False, get_label='name')
	grade = QuerySelectField(query_factory=grade_query, allow_blank=False, get_label='name')

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(NewEmployeeForm, self).__init__(*args, **kwargs)

	def validate_nin(self, nin):
		nin_id = Employee.query.filter_by(nin=nin.data).first()
		if nin_id:
			raise ValidationError('Employee already exists!')

	def validate_email(self, email):
		user_email = Employee.query.filter_by(email=email.data).first()
		if user_email:
			raise ValidationError('Employee already exists!')

class NewDepartmentForm(FlaskForm):
	name = StringField('', validators=[DataRequired('Please fill in the name of the department')])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(NewDepartmentForm, self).__init__(*args, **kwargs)

	def validate_name(self, name):
		department_name = Department.query.filter_by(name=name.data).first()
		if department_name:
			raise ValidationError('Department already exists!')

class NewGradeForm(FlaskForm):
	grade_name = StringField('', validators=[DataRequired('Please fill in the name of the grade')])
	salary = IntegerField('', validators=[DataRequired()])
	department = QuerySelectField(query_factory=department_query, allow_blank=True, get_label='name')

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(NewGradeForm, self).__init__(*args, **kwargs)

class GenerateReportForm(FlaskForm):
	grade = QuerySelectField(query_factory=grade_query, allow_blank=True, get_label='name')
	salary = QuerySelectField(query_factory=grade_query, allow_blank=True, get_label='salary')
	department = QuerySelectField(query_factory=department_query, allow_blank=True, get_label='name')

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(GenerateReportForm, self).__init__(*args, **kwargs)