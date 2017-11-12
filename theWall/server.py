from flask import Flask, render_template, redirect, request, session, flash
import datetime
import re
from mysqlconnection import MySQLConnector
import hashlib
import os, binascii
import md5

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile(r'^[a-zA-Z]+$')
PSWD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,18}$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'thewall')

app.secret_key = "000"

@app.route('/') # ROOT ROUTE
def index():
	return render_template('index.html')

@app.route('/register', methods = ["POST"]) # REGISTER METHOD
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
	elif request.form['pw'] != request.form['pwconfirm']:
		flash('Passwords do not match!')
		is_valid = False
	if is_valid:
		add_user = "INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:fn, :ln, :em, :hashed_pw, :salt, NOW(), NOW())"
		salt = binascii.b2a_hex(os.urandom(15))
		hashed_pw = hashlib.md5( salt + request.form['pw'] ).hexdigest()
		user_data = {	'fn':request.form['fname'],
						'ln':request.form['lname'],
						'em':request.form['email'],
						'hashed_pw':hashed_pw,
						'salt':salt
					}
		user_id = mysql.query_db(add_user, user_data)
		session['name'] = request.form["fname"]
		session['user_id'] = user_id
		return redirect("/wall")
	return redirect('/')

@app.route('/login', methods = ["POST"]) # LOGIN METHOD
def login():
	# is there a user with that email?
	find_user_q = "SELECT * FROM users WHERE email = :email LIMIT 1"
	data = {'email': request.form['email']}
	found_user = mysql.query_db(find_user_q, data)
	
	if len(found_user) == 0:
		flash("No such user with that email")
	else: # if so, does the password they entered match what is in the db?
		encrypted_password = md5.new(found_user[0]['salt'] + request.form['pw']).hexdigest()
		if found_user[0]["password"] != encrypted_password:
			flash("Password is incorrect!")
			flash(found_user[0]['salt'])
			flash(found_user[0]['password'])
		else:
			session['name'] = found_user[0]['first_name']
			session['user_id'] = found_user[0]['id']
			return redirect("/wall")
	return	redirect('/')

@app.route('/wall') # the wall GET request
def show_wall():
	get_all_messages_query = "SELECT message, messages.created_at, messages.id AS id, users.id as user_id, first_name, last_name FROM messages JOIN users ON users.id = messages.user_id" # joining users to messages to get the name!
	all_messages = mysql.query_db(get_all_messages_query)

	get_all_comments_query = "SELECT comment, comments.created_at, comments.message_id AS message_id, comments.id AS id, users.id as user_id, first_name, last_name FROM comments JOIN users ON users.id = comments.user_id" # joining users to comments to get the name!
	all_comments = mysql.query_db(get_all_comments_query)

	return render_template("wall.html", messages = all_messages, comments = all_comments)

@app.route('/addmessage', methods = ["POST"]) # posting messages FROM the wall TO the wall
def add_message():
	add_message_query = "INSERT INTO messages (user_id, message, created_at) VALUES (:user_id, :message, NOW())" # values here correspond to the keys in object below
	data = {'message': request.form['message'],
			'user_id': session['user_id']}
	mysql.query_db(add_message_query, data)
	return redirect('/wall')

@app.route('/addcomment', methods = ["POST"]) # posting comments to messages
def add_comment():
	add_comment_query = "INSERT INTO comments (user_id, message_id, comment, created_at) VALUES (:user_id, :message_id, :comment, NOW())" # values here correspond to the keys in object below
	data = {'comment': request.form['comment'],
			'user_id': session['user_id'],
			'message_id': request.form['messageid']}
	mysql.query_db(add_comment_query, data)
	return redirect('/wall')

@app.route('/logout', methods = ['POST', 'GET']) # logout route, even necessary? or can just link in html back to root?
def log_out():
	session.pop("name")
	session.pop("user_id")
	return redirect("/")

app.run(debug=True)