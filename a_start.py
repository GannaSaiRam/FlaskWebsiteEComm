from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return '<h1>Hello, World</h1>'

@app.route('/about')
def about_page():
	return "<h1>About Page</h1>"

@app.route('/about/<username>')
def about_user(username):
	return "<h1>This page is about the user {}</h1>".format(username)