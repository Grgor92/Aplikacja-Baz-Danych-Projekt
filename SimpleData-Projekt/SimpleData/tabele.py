#import plik app(aplikacje)
from enum import unique
from re import T
from SimpleData import app
#import biblioteki czas
from datetime import datetime
#import pliku z baz danych
from SimpleData import db, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref

# deklaracja funkcji do pobierania użytkownika po jego id unique=True,
@login_manager.user_loader
def load_user(user_id):
    return Uzytkownicy.query.get(int(user_id))

class Kontrahenci(db.Model):
    NIP = db.Column(db.String(15), primary_key=True, unique=True)
    nazwa_firmy = db.Column(db.String(20), nullable=False)
    miasto = db.Column(db.String(50), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    ulica = db.Column(db.String(32), nullable=False)
    numer = db.Column(db.String(32), nullable=False)

    


class Dokumenty(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True, nullable=False)
    numer_dokumentu = db.Column(db.String(20), nullable=False, unique=True)
    data_wystawienia = db.Column(db.Date, nullable=False)
    id_uzytkownika = db.Column(db.String(32), nullable=False)
    NIP_kontrahenta = db.Column(db.String(32), db.ForeignKey('kontrahenci.NIP'))
    typ_dokumentu = db.Column(db.String(32), nullable=False)
    data_wykonania = db.Column(db.Date, nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)
    kontrahent = db.relationship("Kontrahenci", backref=backref('dokumenty', order_by=id_dokumentu))
    
    def __init__(self, numer_dokumentu):
        self.numer_dokumentu = numer_dokumentu
        
    def __repr__(self):
        return "<Numer_dokumentu('%s')>" % self.numer_dokumentu


class Uzytkownicy(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    imie = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    haslo = db.Column(db.String(32), nullable=False)
    typ = db.Column(db.String(30), nullable=False)   

    

    

class Dokumenty_Historyczne(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True)
    numer_dokumentu = db.Column(db.String(20), nullable=False)
    data_wystawienia = db.Column(db.Date)
    id_uzytkownika = db.Column(db.String(32), nullable=False)
    NIP_kontrahenta = db.Column(db.String(32), nullable=False)
    typ_dokumentu = db.Column(db.String(32), nullable=False)
    data_wykonankia = db.Column(db.Date, nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)

class Towary(db.Model):
    id_towaru = db.Column(db.Integer, primary_key=True)
    kod_towaru = db.Column(db.Integer, nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)

class towary_dokument(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True)
    id_towaru = db.Column(db.Integer, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)

class magazyn_towar(db.Model):
    nr_sekcji = db.Column(db.String(32), primary_key=True)
    id_towaru = db.Column(db.Integer, nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)

class Magazyn(db.Model):
    nr_sekcji = db.Column(db.String(32), primary_key=True)
    pojemnosc_sekcji = db.Column(db.Integer, nullable=False)



# deklaracja funkcji do pobierania uzytkownika po jego id unique=True,
@login_manager.user_loader
def load_user(user_id):
    return Uzytkownicy.query.get(int(user_id))