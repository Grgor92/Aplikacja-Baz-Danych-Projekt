# -*- coding: utf-8 -*-
#Import biblioteki
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
app = Flask(__name__)

app.config['SECRET_KEY'] = "e761d6362a5b7811a2b1a7e227e39900"
@app.before_first_request
def init_session():
    session['user'] = None

#Łączenie z bazą danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/sd_baza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import SimpleData.views