import os
import json
from flask import Flask, render_template, request, url_for, redirect, session

import streamfinder.database as db

def run_website():

	template_folder = os.path.join(os.path.dirname(__file__), 'templates')
	static_folder = os.path.join(os.path.dirname(__file__), 'static')
	print("using template folder %s" % template_folder)
	print("using static folder %s" % static_folder)

	app = Flask(__name__,
		template_folder=template_folder,
		static_url_path='/static',
		static_folder=static_folder)

	app.config['SECRET_KEY'] = 'this is a secret that needs to be moved to a config file at some point'

	@app.route('/')
	def index():
		return render_template('index.html', variable_from_python="Hello World!")

	### Example of handling GET request with variable passed through
	@app.route('/exampleGET/<multiplier>', methods=['GET'])
	def exampleGET(multiplier):
		num = request.args.get("number")
		adder = request.args.get("adder")
		return render_template('index.html', variable_from_python=f"After multiplying by {multiplier} and adding {adder}, your result is: {int(num) * int(multiplier) + int(adder)} then also {users}")


	### Example of handling POST request
	@app.route('/examplePOST', methods=['POST'])
	def examplePOST():
		firstName = request.form.get("firstName")
		lastName = request.form.get("lastName")
		return render_template('index.html', variable_from_python="Your last name was: " + lastName)

	app.run(host='0.0.0.0', port='8080', debug=True)
