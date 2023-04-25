# -*- coding: utf-8 -*-
#Import biblioteki
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from datetime import timedelta
import os
app = Flask(__name__)

# generowanie klucza losowego
SECRET_KEY = os.urandom(32)

# ustawienie klucza w konfiguracji aplikacji
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)
@app.before_first_request
def init_session():
    session.permanent = True

#Łączenie z bazą danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/sd_baza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import SimpleData.views