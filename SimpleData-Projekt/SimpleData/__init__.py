# -*- coding: utf-8 -*-
#Import biblioteki
from flask_sqlalchemy import SQLAlchemy
#Bibloteka odpowiedzialna za bezpieczne haszowanie haseł
from flask_bcrypt import Bcrypt

from flask import Flask, session, redirect, url_for, flash
from datetime import timedelta
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)

# generowanie klucza losowego
SECRET_KEY = os.urandom(32)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.sesion = True
@login_manager.unauthorized_handler
def unauthorized():
    flash('Musisz się zalogować, aby uzyskać dostęp do tej strony!', 'danger')
    return redirect(url_for('home'))

@login_manager.needs_refresh_handler
def needs_refresh():
    flash('Twoja sesja wygasła, zaloguj się ponownie!', 'danger')
    return redirect(url_for('logout'))

# ustawienie klucza w konfiguracji aplikacji
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=600)
@app.before_first_request
def init_session():
    session.permanent = True

#Łączenie z bazą danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/sd_baza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
import SimpleData.views
