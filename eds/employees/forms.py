from eds.models import Employee
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators, StringField, PasswordField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

banks = [('Access Bank', 'Access Bank'), ('Access Bank (Diamond)', 'Access Bank (Diamond)'), ('ALAT by WEMA', 'ALAT by WEMA'), ('ASO Savings and Loans', 'ASO Savings and Loans'), ('CEMCS Microfinance Bank', 'CEMCS Microfinance Bank'), ('Citibank Nigeria', 'Citibank Nigeria'), ('Ecobank Nigeria', 'Ecobank Nigeria'), ('Ekondo Microfinance Bank', 'Ekondo Microfinance Bank'), ('Fidelity Bank', 'Fidelity Bank'), ('First Bank of Nigeria', 'First Bank of Nigeria'), ('First City Monument Bank', 'First City Monument Bank'), ('Globus Bank', 'Globus Bank'), ('Guaranty Trust Bank', 'Guaranty Trust Bank'), ('Hasal Microfinance Bank', 'Hasal Microfinance Bank'), ('Heritage Bank', 'Heritage Bank'), ('Jaiz Bank', 'Jaiz Bank'), ('Keystone Bank', 'Keystone Bank'), ('Kuda Bank', 'Kuda Bank'), ('Parallex Bank', 'Parallex Bank'), ('Polaris Bank', 'Polaris Bank'), ('Providus Bank', 'Providus Bank'), ('Rubies MFB', 'Rubies MFB'), ('Sparkle Microfinance Bank', 'Sparkle Microfinance Bank'), ('Stanbic IBTC Bank', 'Stanbic IBTC Bank'), ('Standard Chartered Bank', 'Standard Chartered Bank'), ('Sterling Bank', 'Sterling Bank'), ('Suntrust Bank', 'Suntrust Bank'), ('TAJ Bank', 'TAJ Bank'), ('TCF MFB', 'TCF MFB'), ('Titan Bank', 'Titan Bank'), ('Union Bank of Nigeria', 'Union Bank of Nigeria'), ('United Bank For Africa', 'United Bank For Africa'), ('Unity Bank', 'Unity Bank'), ('VFD', 'VFD'), ('Wema Bank', 'Wema Bank'), ('Zenith Bank', 'Zenith Bank')]


class EmployeeLogForm(FlaskForm):
	email = StringField('', validators=[DataRequired('Please fill in a your email address')])
	password = PasswordField('', validators=[DataRequired('Please fill in your password'), Length(min=6)])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(EmployeeLogForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(FlaskForm):
	oldpassword = PasswordField('',
		validators=[DataRequired('Please fill in your old password')])
	newpassword = PasswordField('',
		validators=[DataRequired('Please fill in your new password'), Length(min=6)])
	confirmnewpassword = PasswordField('',
		validators=[EqualTo('newpassword')])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(ChangePasswordForm, self).__init__(*args, **kwargs) 

class PaymentSettingsForm(FlaskForm):
	phone = StringField('', validators=[DataRequired('Please fill in this field')])
	bank_name = SelectField('', choices=banks, validators=[DataRequired('Please fill in this field')])
	acc_name = StringField('', validators=[DataRequired('Please fill in this field')])
	acc_number = StringField('', validators=[DataRequired('Please fill in this field')])

	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = False
		super(PaymentSettingsForm, self).__init__(*args, **kwargs)