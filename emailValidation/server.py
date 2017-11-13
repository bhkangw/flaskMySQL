from flask import Flask, redirect, render_template, request, flash, session
import datetime
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'emailvalidation')
app.secret_key = "000"

@app.route('/')
def index ():
	return render_template('index.html')

@app.route('/add_email', methods = ['POST'])
def add_email():
	session["email"] = request.form['email'] # creating a session onject in order to recall the email when displaying it on the success page
	if len(request.form['email']) < 1:
		flash('Email cannot be empty!')
		return render_template('index.html')
	elif not EMAIL_REGEX.match(request.form['email']):
		flash('Email is not valid!')
		return render_template('index.html')
	else:
		check_email_query = "SELECT * FROM emails WHERE emails.email = '{}'".format(request.form['email']) # is creating the string to run as a query
		validemails = mysql.query_db(check_email_query) # this line runs the string (var validemails) as a query through mySQL
		if len(validemails) > 0: # because the result of the query is given back as a list, checking if the length > 0 confirms if the entry exists or not
			flash('Email exists!')
			return render_template('index.html')
		else: # if it returns back as 0, it means the email is valid and can continue on with the insertion into the table
			add_email_query = "INSERT INTO emails (email, email_added) VALUES (:email, :email_added)" 
			data = {'email': request.form['email'],
					'email_added': datetime.datetime.now()
					}
			mysql.query_db(add_email_query, data)
			return redirect('/success')

@app.route('/success')
def show():
	get_all_emails_query = "SELECT * FROM emails"
	all_emails = mysql.query_db(get_all_emails_query)
	# myemail = request.form['email']
	return render_template('success.html', emails = all_emails, emailz = session["email"])

app.run(debug=True)