from flask import Flask, render_template, redirect, request
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app,'friends')

@app.route('/')
def index():
	get_all_friends_query = "SELECT * FROM friends"
	all_friends = mysql.query_db(get_all_friends_query)
	return render_template('index.html', friends = all_friends) # friends = is how we send data to HTML via jinja

@app.route('/add_friend', methods = ['POST'])
def add_friend():
	add_friends_query = "INSERT INTO friends (name, age, friend_since) VALUES (:name, :age, :friend_since)" # values here correspond to the keys in object below
	data = {'name': request.form['name'], 
			'age': request.form['age'], 
			'friend_since': request.form['friend_since']}
	mysql.query_db(add_friends_query, data)
	return redirect('/')

app.run(debug=True)