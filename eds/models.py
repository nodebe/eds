from eds import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
	id = db.Column(db.Integer,  primary_key=True)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(120), nullable=False)
	user_status = db.Column(db.String(7), default='admin')


class Employee(db.Model):
	id = db.Column(db.Integer,  primary_key=True)
	firstname = db.Column(db.String(30), nullable=False)
	lastname = db.Column(db.String(30), nullable=False)
	dob = db.Column(db.String(), nullable=False)
	doj = db.Column(db.String(), nullable=False)
	address = db.Column(db.String(120), nullable=False)
	city = db.Column(db.String(40), nullable=False)
	state = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	phone = db.Column(db.String(15), default='')
	nin = db.Column(db.String(12), default='')
	id_card = db.Column(db.Text)
	password = db.Column(db.String(120), nullable=False)
	user_status = db.Column(db.String(7), default='member')
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'))

class Department(db.Model):
	id = db.Column(db.Integer,  primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	employees = db.relationship('Employee', backref='employee_department')
	grades = db.relationship('Grade', backref='grade_department')

class Grade(db.Model):
	id = db.Column(db.Integer,  primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	salary = db.Column(db.String(20), nullable=False)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	employees = db.relationship('Employee', backref='employee_grade')