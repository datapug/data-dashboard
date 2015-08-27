import flask
from flask import Flask, request, redirect, url_for, render_template, make_response, session, flash, g
from functools import wraps
import sqlite3
from sqlalchemy import create_engine # db connection
import datetime as dt
import plotly.plotly as py
from plotly.graph_objs import Bar, Scatter, Marker, Layout
import pandas as pd
import numpy as np

#---------------------------------------------------------------------------
# app initialization 
app = Flask(__name__)
app.secret_key = 'topsecretkeythatyouwillneverguess'

# initialize the sqlite database
disk_engine = create_engine('sqlite:///fruits.db')

'''
app.database = 'fruits.db'
def connect_db():
    return sqlite3.connect(app.database)
'''
#---------------------------------------------------------------------------
# Static pages including fruit database interaction
# this login_required has to be before any @login_required decoraters are called in the script
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login.')
            return redirect(url_for('login'))
    return wrap

@app.route('/fruits')
@login_required
def fruits():
    args = flask.request.args
    selected_farmer = flask.request.values.get("selected_farmer", "Bob")
    selected_fruit = flask.request.values.get("selected_fruit", "Apple")

    return render_template('fruits.html',
                           selected_farmer=selected_farmer,
                           selected_fruit=selected_fruit)

    # database sqlite3 basic query method (paired with above database connection)
    # g is used for storing temporary data
    g.db = connect_db()
    cur = g.db.execute('select * from fruits')
    cur_farmer = g.db.execute('select * from farmer')
    fruits = [dict(fruit=row[0], price=row[1]) for row in cur.fetchall()]
    farmer = [dict(fruit=row[0], farmer=row[1], state=row[2]) for row in cur_farmer.fetchall()]
    g.db.close()
    return render_template('fruits.html', fruits=fruits, farmer=farmer, selected_farmer=selected_farmer)

#---------------------------------------------------------------------------
# Plot/Dashboard route

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

#---------------------------------------------------------------------------
# Login/logout routes and login_required (wraps, @login_required to routes,
# session key, and secret key)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            # flash('You were just logged in!')
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None) #none is popped into logged_in
    flash('You have logged out.')
    return redirect(url_for('login'))

#---------------------------------------------------------------------------
# server initialization and start
if __name__ == '__main__':
    #app.run(debug=False) # this is on a private local server
    app.run(host='0.0.0.0', debug=True)
