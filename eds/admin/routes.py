from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from eds.utils import save_picture, decode_picture
from eds.admin.forms import AdminRegForm, AdminLogForm, NewEmployeeForm, NewDepartmentForm, NewGradeForm, GenerateReportForm
from eds.models import Admin, Employee, Department, Grade
from eds import db
from passlib.hash import sha256_crypt as sha256
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime as dt

admin = Blueprint('admin', __name__)

date = dt.now()
notification_date = date.strftime('%Y-%b-%d')

error_message = 'Something went wrong! '

@admin.route('/adminsignin', methods=['GET','POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('admin.admindashboard'))
	form = AdminLogForm()
	if form.validate_on_submit():
		try:
			user = Admin.query.filter_by(email=form.email.data).first()
			if user and sha256.verify(form.password.data, user.password):
				login_user(user)
				return redirect(url_for('admin.admindashboard'))
			else:
				flash('Login unsuccessful. Email/Password not valid', 'warning')
				return redirect(url_for('admin.signin'))
			
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('adminsignin.html', title='Admin Login', form=form)


@admin.route('/adminsignup', methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('admin.admindashboard'))
	form = AdminRegForm()
	hashed_password = sha256.encrypt(str(form.password.data))
	if form.validate_on_submit():
		try:
			admin = Admin(username=form.username.data,email=form.email.data,password=hashed_password)
			db.session.add(admin)
			db.session.commit()
			flash('Admin account created successfully.', 'success')
			login_user(admin)
			return redirect(url_for('admin.admindashboard'))
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('adminsignup.html', title='Admin Signup', form=form)

@admin.route('/admindashboard')
def admindashboard():

	return render_template('admindashboard.html', title='Admin Dashboard')

@admin.route('/createnewemployee', methods=['GET','POST'])
def createnewemployee():
	if current_user.user_status != 'admin':
		abort(403) 
	form = NewEmployeeForm()

	if form.validate_on_submit():
		try:
			hashed_password = sha256.encrypt(str(form.lastname.data))
			encode_image = save_picture(form.id_card.data)
			employee = Employee(firstname=form.firstname.data,lastname=form.lastname.data,dob=form.dob.data,doj=form.doj.data,address=form.address.data,city=form.city.data,state=form.state.data,email=form.email.data,phone=form.phone.data,nin=str(form.nin.data),password=hashed_password,department_id=form.department.data.id,grade_id=form.grade.data.id,id_card=encode_image)
			db.session.add(employee)
			db.session.commit()
			flash('Employee created successfully', 'success')
			return redirect(url_for('admin.createnewemployee'))
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('createnewemployee.html', title='Create New Employee', form=form)

@admin.route('/createnewdepartment', methods=['GET','POST'])
def createnewdepartment():
	if current_user.user_status != 'admin':
		abort(403)
	form = NewDepartmentForm()
	if form.validate_on_submit():
		try:
			department = Department(name=form.name.data)
			db.session.add(department)
			db.session.commit()
			flash('Department created successfully', 'success')
			return redirect(url_for('admin.createnewdepartment'))
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('createnewdepartment.html',title='Create New Department', form=form)

@admin.route('/createnewgrade', methods=['GET','POST'])
def createnewgrade():
	if current_user.user_status != 'admin':
		abort(403)
	form = NewGradeForm()
	if form.validate_on_submit():
		try:
			grade_name = Grade.query.filter_by(name=form.grade_name.data, department_id=form.department.data.id).first()
			if grade_name:
				flash('Grade already exists!', 'warning')
				return redirect(url_for('admin.createnewgrade'))
			grade = Grade(name=form.grade_name.data,salary=form.salary.data,department_id=form.department.data.id)
			db.session.add(grade)
			db.session.commit()
			flash('Grade added successfully', 'success')
			return redirect(url_for('admin.createnewgrade'))
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('createnewgrade.html', title='Create New Grade', form=form)

@admin.route('/generatereport', methods=['GET','POST'])
def generatereport():
	if current_user.user_status != 'admin':
		abort(403)
	report = Employee.query.all()
	department_employees, grade_employees, salary_employees, doj_employees = [],[],[],[]
	form = GenerateReportForm()
	if form.validate_on_submit():
		try:
			if form.department.data != None:
				department_employees = Department.query.filter_by(name=form.department.data.name).first().employees
				report = list(set(report).intersection(department_employees))

			if form.grade.data != None:
				grade_employees = Grade.query.filter_by(name=form.grade.data.name).first().employees
				report = list(set(report).intersection(grade_employees))

			if form.salary.data != None:
				salary_employees = Grade.query.filter_by(salary=form.salary.data.salary).first().employees
				report = list(set(report).intersection(salary_employees))
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('generatereport.html', title='Generate Report', form=form, report=report)
