#import plik app(aplikacje)
from enum import unique
from re import T
from SimpleData import app
#import biblioteki czas
from datetime import datetime
#import pliku z baz danych
from SimpleData import db, login_manager
from flask_login import UserMixin

# deklaracja funkcji do pobierania u¿ytkownika po jego id unique=True,
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Kontrahenci(db.Model):
    NIP = db.Column(db.String(15), primary_key=True, unique=True)
    nazwa_firmy = db.Column(db.String(20), nullable=False)
    miasto = db.Column(db.String(50), nullable=False)
    telefon = db.Column(db.Integer(11), nullable=False)
    ulica = db.Column(db.String(32), nullable=False)
    numer = db.Column(db.String(32), nullable=False)


class Dokumenty(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True, nullable=False)
    numer_dokumentu = db.Column(db.String(20), nullable=False, unique=True)
    data_wystawienia = db.Column(db.date, nullable=False)
    id_uzytkownika = db.Column(db.String(32), nullable=False)
    NIP_kontrahenta = db.Column(db.String(32), nullable=False)
    typ_dokumentu = db.Column(db.ENUM(32), nullable=False)
    data_wykonania = db.Column(db.date, nullable=False)
    data_waznosci_towaru = db.Column(db.date, nullable=False)


class Uzytkownicy(db.Model):
    id_uzytkownika = db.Column(db.String(15), primary_key=True, unique=True)
    imie = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    haslo = db.Column(db.Integer(32), nullable=False)
    typ = db.Column(db.ENUM, nullable=False)

class Dokumenty_Historyczne(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True)
    numer_dokumentu = db.Column(db.String(20), nullable=False)
    data_wystawienia = db.Column(db.date)
    id_uzytkownika = db.Column(db.String(32), nullable=False)
    NIP_kontrahenta = db.Column(db.String(32), nullable=False)
    typ_dokumentu = db.Column(db.ENUM(32), nullable=False)
    data_wykonankia = db.Column(db.date, nullable=False)
    data_waznosci_towaru = db.Column(db.date, nullable=False)

class Towary(db.Model):
    id_towaru = db.Column(db.Integer(32), primary_key=True)
    kod_towaru = db.Column(db.Integer(20), nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    data_waznosci_towaru = db.Column(db.date, nullable=False)

class towary_dokument(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True)
    id_towaru = db.Column(db.Integer(20), nullable=False)
    ilosc = db.Column(db.Integer(20), nullable=False)
    data_waznosci_towaru = db.Column(db.date, nullable=False)

class magazyn_towar(db.Model):
    nr_sekcji = db.Column(db.String(32), primary_key=True)
    id_towaru = db.Column(db.Integer(20), nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    data_waznosci_towaru = db.Column(db.date, nullable=False)

class Magazyn(db.Model):
    nr_sekcji = db.Column(db.String(32), primary_key=True)
    pojemnosc_sekcji = db.Column(db.Integer(20), nullable=False)