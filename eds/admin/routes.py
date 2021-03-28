from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
#from eds.admin.forms import FAQForm
from eds.models import Admin, Employee
from eds import db
from datetime import datetime as dt

admin = Blueprint('admin', __name__)

date = dt.now()
notification_date = date.strftime('%Y-%b-%d')

@admin.route('/adminsignin', methods=['GET','POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('admin.admindashboard'))
	form = EmployeeLogForm()
	if form.validate_on_submit():
		try:
			user = Admin.query.filter_by(email=form.email.data).first()
			if user and sha256.verify(form.password.data, user.password):
				login_user(user)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('admin.admindashboard'))
			else:
				flash('Login unsuccessful. Email/Password not valid', 'warning')
			
		except Exception as e:
			flash(error_message+str(e), 'warning')
	return render_template('adminsignin.html', title='Login', form=form)


@admin.route('/admindashboard')
def admindashboard():

	return render_template('admindashboard.html', title='Admin Dashboard')