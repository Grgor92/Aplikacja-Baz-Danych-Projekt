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
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import backref
# deklaracja funkcji do pobierania uzytkownika po jego id unique=True,

@login_manager.user_loader
def load_user(user_id):
    return Uzytkownicy.query.get(int(user_id))

class Kontrahenci(db.Model):
    #NIP - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli Dokumenty przez Kontrahenta. Krotke NIP.
    NIP = db.relationship('Dokumenty', backref='owner'),db.Column(db.Integer, primary_key=True, unique=True)
    nazwa_firmy = db.Column(db.String(20), nullable=False)
    miasto = db.Column(db.String(50), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    ulica = db.Column(db.String(32), nullable=False)
    numer = db.Column(db.String(32), nullable=False)


    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<nazwa_firmy('%s')>" % self.nazwa_firmy % "<NIP('%s')>" % self.NIP

    


class Dokumenty(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True, nullable=False)
    numer_dokumentu = db.Column(db.String(20), nullable=False, unique=True)
    data_wystawienia = db.Column(db.Date, nullable=False)
    #id_uzytkownika - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli  towary_dokument przez Dokumenty. | NIP relacja jeden do wielu. Klucz obcy to id_uzytkownika
    id_uzytkownika = db.relationship('towary_dokument', backref='owner'), db.Column(db.Date, nullable=False), db.Column(db.Integer, db.ForeignKey('id.uzytkownika'))
    #NIP relacja jeden do wielu. Klucz obcy to NIP_kontrahenta
    NIP_kontrahenta = db.Column(db.Integer, db.ForeignKey('NIP.kontrahenta'))
    typ_dokumentu = db.Column(db.String(32), nullable=False)
    data_wykonania = db.Column(db.Date, nullable=False)
    #data_waznosci_towaru - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli  towary_dokument przez Dokumenty.
    data_waznosci_towaru = db.relationship('towary_dokument', backref='owner') ,db.Column(db.Date, nullable=False)
    kontrahent = db.relationship("Kontrahenci", backref=backref('dokumenty', order_by=id_dokumentu))
    
    def __init__(self, numer_dokumentu):
        self.numer_dokumentu = numer_dokumentu
        
    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<Numer_dokumentu('%s')>" % self.numer_dokumentu % "<data_wystawienia(%s)>" % self.data_wystawienia


class Uzytkownicy(db.Model, UserMixin):
    #id - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli Dokumenty przez Uzytkownicy.
    id = db.relationship('Dokumenty', backref='owner'), db.Column(db.Integer, primary_key=True, unique=True)
    imie = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    haslo = db.Column(db.String(32), nullable=False)
    typ = db.Column(db.String(30), nullable=False)  
    
    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<email('%s')>" % self.email % "<typ/stanowisko('%s')>" % self.type % "<imie('%s')>" % self.imie

    

    

class Dokumenty_Historyczne(db.Model):
    id_dokumentu = db.Column(db.String(32), primary_key=True)
    numer_dokumentu = db.Column(db.String(20), nullable=False)
    data_wystawienia = db.Column(db.Date)
    id_uzytkownika = db.Column(db.String(32), nullable=False)
    NIP_kontrahenta = db.Column(db.String(32), nullable=False)
    typ_dokumentu = db.Column(db.String(32), nullable=False)
    data_wykonankia = db.Column(db.Date, nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)
    
    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<numer_dokumentu('%s')>" % self.numer_dokumentu % "<data_wystawienia('%s')>" % self.data_wystawienia % "<NIP_kontrahenta('%s')>" % self.NIP_kontrahenta
#relacja wiele  do wielu.
Towary_magazyn_towar = db.Table('Towary_magazyn_towar',
    db.Column('Towary_id_towaru', db.Integer, db.ForeignKey('Towary.id.towaru')),
    db.Column('magazyn_towar_id_towaru', db.Integer, db.ForeignKey('towary.magazyn.id.towaru')),
    )
class Towary(db.Model):
    #id_towaru - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli towary_dokument przez Towary.
    id_towaru = db.relationship('towary_dokument', backref='owner'), db.Column(db.Integer, primary_key=True)
    kod_towaru = db.Column(db.Integer, nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    data_waznosci_towaru = db.Column(db.Date, nullable=False)
    #relacja wiele do wielu
    following = db.relationship('db.magazyn_towar', secondary=db.Towary_magazyn_towar, backref='followers')

    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<id_towaru('%s')>" % self.id_towaru % "kod_towaru('%s')>" % self.kod_towaru % "<rodzaj('%s')>" % self.rodzaj % "<data_waznosci_towaru('%s')>" % self.data_waznosci_towaru

class towary_dokument(db.Model):
    #id_dokumentu relacja jeden do wielu. Klucz obcy to id_dokumentu
    id_dokumentu = db.Column(db.String(32), primary_key=True), db.ForeignKey('id.dokumentu')
    #id_towaru relacja jeden do wielu. Klucz obcy to id_towaru
    id_towaru = db.Column(db.Integer, nullable=False), db.ForeignKey('id_towaru')
    ilosc = db.Column(db.Integer, nullable=False)
    #data_waznosci_towaru relacja jeden do wielu. Klucz obcy to data_waznosci_towaru | #data_waznosci_towaru - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli magazyn_towar przez towary_dokument.
    data_waznosci_towaru =db.relationship('magazyn_towar', backref='owner'), db.Column(db.Date, nullable=False), db.ForeignKey('data.waznosci.towaru')

    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<id_dokumentu(%s)>" % self.id_dokumentu % "<id_towaru(%s)>" % self.id_towaru % "<ilosc(%s)>" % self.ilosc % "<data_waznosci_towaru(%s)>" % self.data_waznosci_towaru

class magazyn_towar(db.Model):
    #nr_sekcji relacja jeden do wielu. Klucz obcy to nr_sekcji
    nr_sekcji = db.Column(db.String(32), primary_key=True), db.ForeignKey('nr.sekcji')
    id_towaru = db.Column(db.Integer, nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)
    #data_waznosci_towaru relacja jeden do wielu. Klucz obcy to data_waznosci_towaru
    data_waznosci_towaru = db.Column(db.Date, nullable=False), db.ForeignKey('data.waznosci.towaru')

    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<nr_sekcji('s%')>" % self.nr_sekcji % "<id_towaru('s%')>" % self.id_towaru %  "<rodzaj('s%')>" % self.rodzaj % "<ilosc('s%')>" % self.ilosc % "<data_waznosci_towaru('s%')>" % self.data_waznosci_towaru 

class Magazyn(db.Model):
    #nr_sekcji - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli magazyn_towar przez Magazyn.
    nr_sekcji =db.relationship('magazyn_towar', backref='owner'), db.Column(db.String(32), primary_key=True)
    pojemnosc_sekcji = db.Column(db.Integer, nullable=False)

    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<nr_sekcji('s%')>" % self.nr_sekcji % "<pojemnosc_sekcji('s%')>" % self.pojemnosc_sekcji
