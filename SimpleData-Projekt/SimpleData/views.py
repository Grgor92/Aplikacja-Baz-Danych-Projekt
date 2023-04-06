# -*- coding: utf-8 -*-

from flask import render_template, jsonify, redirect, url_for
from SimpleData import app

from datetime import datetime

from forms import RegistrationForm, LoginForm

@app.route('/api/time', )
def current_time():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y %H:%M")
    return jsonify({'time': formatted_now})

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        "home.html",
        title = "SimpleData"
    )

@app.route('/login')
def login():
    form = LoginForm
    return render_template(
        "login.html",
        title = "Logowanie",
        form=form 
        )
@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('rejestruj.html', 
        title='Rejestracja',
        form=form
        )
