#!/bin/python

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return 'Welcome!'

@app.route('/test/<test_in>')
def test(test_in):
	return render_template("test.html", test_in = test_in)

@app.route('/view')
@app.route('/view/<path:my_path>', methods=['GET', 'POST'])
def data(my_path=None):
	if request.method == 'POST':
		return 'Using post'
	else:
		return my_path if my_path is not None else 'No path'
def dir():
	if request.method == 'POST':
		do_edit_dir()
	else:
		show_dir()
def json():
	if request.method == 'POST':
		do_edit_json()
	else:
		show_json()
def temp():
	if request.method == 'POST':
		do_edit_temp()
	else:
		show_temp()

url_for('static', filename='')

if __name__ == '__main__':
	app.run(debug=True)
