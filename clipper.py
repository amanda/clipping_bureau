#!usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, os
from flask import Flask, request, g, redirect, url_for, render_template
from contextlib import closing

#TODO: test database getting and writing somehow, templates!

DATABASE = 'clipper.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__) #switch to config.py file later

#database funcs
def connect_db():
	return sqlite3.connect(app.config['DATABASE']) #returns a connection object

def init_db(): #run before running app
	with closing(connect_db()) as db: #connection is called db
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db() #connect to the database before asking it for stuff

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

#routing and updating database from forms
@app.route('/')
def index():
	'''shows form to enter a new clip'''
	return render_template('index.html')

@app.route('/clips')
def show_clips():
	'''show all saved clips, most recent at top'''
	cur = g.db.execute('select clip from clips order by id desc')
	clips = [c[0] for c in cur.fetchall()]
	return render_template('clips.html', clips=clips)
	
@app.route('/add', methods = ['POST'])
def add_clip():
	'''adds clips to db, redirects to show all clips'''
	g.db.execute('insert into clips (clip) values (?)', [request.form['clip']])
	g.db.commit()
	return redirect(url_for('show_clips'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
