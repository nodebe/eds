from flask import Flask, Blueprint, request, render_template, session, flash, redirect, url_for
from eds.employees.forms import EmployeeLogForm, ChangePasswordForm
from eds import db, app
from passlib.hash import sha256_crypt as sha256
from flask_login import login_user, current_user, logout_user, login_required
from eds.models import Employee
from datetime import datetime as dt


employees = Blueprint('employees', __name__)
error_message = 'Error from our side, please try again later '

@employees.route('/signin', methods=['GET','POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('employees.userdashboard'))
	form = EmployeeLogForm()
	if form.validate_on_submit():
		try:
			user = Employee.query.filter_by(email=form.email.data).first()
			if user and sha256.verify(form.password.data, user.password):
				if user.account_status == 'active':
					login_user(user)
					next_page = request.args.get('next')
					return redirect(next_page) if next_page else redirect(url_for('employees.userdashboard'))
				else:
					flash('Login unsuccessful. Account suspended!', 'warning')
			else:
				flash('Login unsuccessful. Email/Password not valid', 'warning')
			
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('signin.html', title='Login', form=form)

@employees.route('/userdashboard')
@login_required
def userdashboard():
	
	return render_template('userdashboard.html', title='Dashboard')


@employees.route('/userprofile')
@login_required
def userprofile():
	form = EmployeeRegForm()
	pform = ChangePasswordForm()
	form.username.data = current_user.username
	form.email.data = current_user.email
	return render_template('userprofile.html', title='Profile', form=form, pform=pform)

@employees.route('/changepassword', methods=['POST'])
@login_required
def changepassword():
	pform = ChangePasswordForm()
	if pform.validate_on_submit():
		try:
			if sha256.verify(pform.oldpassword.data, current_user.password):
				current_user.password = sha256.encrypt(str(pform.newpassword.data))
				db.session.commit()
				flash('Password changed successfully', 'success')
			else:
				flash('Your password does not match', 'info')
		except Exception as e:
			flash(error_message, 'warning')
		finally:
			return redirect(url_for('employees.userprofile'))
	else:	
		flash('Your password does not match', 'info')
		return redirect(url_for('employees.userprofile'))
	return redirect(url_for('employees.userprofile'))


@employees.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))
