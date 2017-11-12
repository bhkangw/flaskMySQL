from flask import Flask, render_template, redirect, request, session, flash
import datetime
import re
from mysqlconnection import MySQLConnector
from hashlib import md5

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile(r'^[a-zA-Z]+$')
PSWD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,18}$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'thewall')

app.secret_key = "000"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods = ["POST"])
def register():
	is_valid = True
	if len(request.form['email']) < 1:
		flash('Email cannot be empty!')
		is_valid = False
	elif not EMAIL_REGEX.match(request.form['email']):
		flash('Must enter a valid email!')
		is_valid = False
	if len(request.form['fname']) < 1:
		flash('First name cannot be empty!')
		is_valid = False
	elif not NAME_REGEX.match(request.form['fname']):
		flash('Name cannot contain numbers!!')
		is_valid = False
	if len(request.form['lname']) < 1:
		flash('Last name cannot be empty!')
		is_valid = False
	elif not NAME_REGEX.match(request.form['lname']):
		flash('Name cannot contain numbers!!')
		is_valid = False
	if len(request.form['pw']) < 8:
		flash('Password must be at least 8 characters!')
		is_valid = False
	# elif not PSWD_REGEX.match(request.form['email']):
	# 	flash('Password must contain number, lower case, upper case and special characters!')
	elif request.form['pw'] != request.form['pwconfirm']:
		flash('Passwords do not match!')
		is_valid = False
	if is_valid:
		add_user = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:fn, :ln, :em, :pw, NOW(), NOW())"
		user_data = {	'fn':request.form['fname'],
						'ln':request.form['lname'],
						'em':request.form['email'],
						'pw':request.form['pw']
					}
		user_id = mysql.query_db(add_user, user_data)
		session['name'] = request.form["fname"]
		session['user_id'] = user_id
		return redirect("/wall")

	return redirect('/')

@app.route('/login', methods = ["POST"])
def login():
	# is there a user with that email?
	find_user_q = "SELECT * FROM users WHERE email = :email"
	data = {'email': request.form['email']}
	found_user = mysql.query_db(find_user_q, data)
	
	if len(found_user) == 0:
		flash("No such user with that email")
	else: # if so, does the password they entered match what is in the db?
		if found_user[0]["password"] != request.form["pw"]:
			flash("Password is incorrect!")
		else:
			session['name'] = found_user[0]['first_name']
			session['user_id'] = found_user[0]['id']
			return redirect("/wall")
	return	redirect('/')

@app.route('/wall')
def show_wall():
	return render_template("wall.html")



app.run(debug=True)