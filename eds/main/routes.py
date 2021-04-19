from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from eds import db

main = Blueprint('main', __name__)

@main.route('/index')
@main.route('/')
def index():
	return(render_template('index.html', title='Homepage'))