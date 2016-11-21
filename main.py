#!/usr/bin/python
#from __future__ import print_function # In python 2.7
from flask import Flask
from flask import session
from flask import request
from flask import jsonify
from flask import render_template, flash, redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from time import sleep


import json


import string
import random
import models
import sys

import os

PORT = os.environ['flight2vec_PORT']
FORMSECRET = os.environ['flight2vec_FORMSECRET']

def log(msg):
	from datetime import datetime
	import os
	ts = datetime.now()
	print("%s - %s: %s" % (os.path.basename(__file__), ts, msg))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["APPLICATION_ROOT"] = "/"
app.config['SECRET_KEY'] = FORMSECRET
sessionsecret = id_generator(size=10)


users = {'user':os.environ['flight2vec_PASS']}

@app.route('/')
def index(num=0):
	if 'auth' in session.keys():
		if session['auth']==sessionsecret:
			user = session['user']
			return render_template('index.html',results=[],code='')
		else:
			return redirect('/login')
	else:
		return redirect('/login')

@app.route('/similarity', methods=['GET'])
def similarity():
	if 'auth' in session.keys():
		if session['auth']==sessionsecret:
			value = request.args.get('code')
			title = request.args.get('title')
			results,dictionary = models.get_top(value)
			return render_template('index.html',results=results,code=value,title=title,dictionary=dictionary)
		else:
			return redirect('/login')
	else:
		return redirect('/login')


@app.route('/login', methods=['GET','POST'])
def login():
	if 'auth' in session.keys():
		if session['auth']==sessionsecret:
			return redirect('/')
	form = LoginForm()
	if form.validate_on_submit():
		user = form.user.data
		password = form.password.data
		if user in users.keys():
			if users[user] == password:
				session['auth']=sessionsecret
				session['user']=user
				return redirect('/')
			else:
				flash('Wrong password!')
		else:
				flash('Wrong user!')
	
	return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
def logout():
	if 'auth' in session.keys():
		session['auth']=""

	return redirect('/login')



@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    value = request.args.get('term')
    data_list = models.filter_codes(value)
    jdata = json.dumps(data_list)
    return jdata

class LoginForm(Form):
	user = StringField('User id')
	password = PasswordField('Password')
	submit = SubmitField('Login')

if __name__ == '__main__':
	app.run(debug=False, host= '0.0.0.0', port=PORT)
