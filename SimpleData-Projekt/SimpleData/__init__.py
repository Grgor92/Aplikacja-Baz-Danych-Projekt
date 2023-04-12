# -*- coding: utf-8 -*-
from flask import Flask, session
app = Flask(__name__)

app.config['SECRET_KEY'] = "e761d6362a5b7811a2b1a7e227e39900"
@app.before_first_request
def init_session():
    session['user'] = None
import SimpleData.views

