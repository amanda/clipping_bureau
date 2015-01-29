#!usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, os
from flask import Flask, request, g, redirect, url_for, render_template, flash
from contextlib import closing
from flask.ext.cors import CORS

DATABASE = 'clipper.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__) #switch to config.py file later

#allow cross-origin request sharing for posting clips from web
cors = CORS(app)

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
	cur = g.db.execute('select clip, id from clips order by id desc')
	clips = [{"clip": row[0], "id": row[1]} for row in cur.fetchall()]
	return render_template('clips.html', clips=clips)
	
@app.route('/add', methods = ['POST'])
def add_clip():
	'''adds clips to db, redirects to show all clips'''
	g.db.execute('insert into clips (clip) values (?)', [request.form['clip']])
	g.db.commit()
	return redirect(url_for('show_clips'))

@app.route('/delete/<int:clip_id>')
def delete_clip(clip_id):
	'''removes clip from the db'''
	g.db.execute('delete from clips where id=' + str(clip_id))
	g.db.commit()
	flash('clip was successfully deleted.')
	return redirect(url_for('show_clips'))

@app.route('/add_from_web', methods = ['POST'])
def add_from_web():
	g.db.execute('insert into clips (clip) values (?)', [request.args.get('content')])
	g.db.commit()
	return "saved clip from web"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
