#import plik app(aplikacje)
from SimpleData import app
#import biblioteki czas
from datetime import datetime
#import pliku z baz¹ danych
from SimpleData import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50))
    haslo = db.Column(db.String(32), nullable=False)