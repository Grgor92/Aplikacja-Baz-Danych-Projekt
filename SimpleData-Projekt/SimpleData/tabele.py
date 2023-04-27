#import plik app(aplikacje)
from enum import unique
from re import T
from SimpleData import app
#import biblioteki czas
from datetime import datetime
#import pliku z baz danych
from SimpleData import db, login_manager
from flask_login import UserMixin

# deklaracja funkcji do pobierania użytkownika po jego id unique=True,
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50))
    haslo = db.Column(db.String(32), nullable=False)
    uprawnienia = db.Column(db.String(32), nullable=False)