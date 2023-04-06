# -*- coding: utf-8 -*-

from flask import render_template, jsonify, redirect, url_for
from SimpleData import app
from datetime import datetime



@app.route('/')
@app.route('/home')
def home():
    return render_template(
        "home.html",
        title = "SimpleData"
    )


@app.route('/api/time', )
def current_time():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y %H:%M")
    return jsonify({'time': formatted_now})

@app.route('/login')
def login():

    return render_template(
        "login.html",
        title = "Logowanie"
        
        )
  

