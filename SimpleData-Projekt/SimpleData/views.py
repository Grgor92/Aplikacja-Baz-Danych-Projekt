# -*- coding: utf-8 -*-

from enum import Flag
from flask import render_template, jsonify, redirect, url_for
from SimpleData import app
from flask import flash
from datetime import datetime
from .forms import RegistrationForm, LoginForm


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

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@sd.com' and form.haslo.data == 'haslo':
            flash('Udało się zalogować', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logowanie nie udane. Sprawdź poprawność danych a wrazie dalszych problemów skontaktuj się z administratorem', 'danger')
    return render_template(
        "login.html",
        title = "Logowanie",
        form=form 
        )
@app.route('/rejestruj', methods=['GET', 'POST'])
def rejestr():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.Nazwa.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('rejestr.html', 
        title='Rejestracja',
        form=form
        )
