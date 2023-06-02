from enum import unique
from re import T
from SimpleData import app, bcrypt
#import biblioteki czas
from datetime import datetime
#import pliku z baz danych
from SimpleData import db, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import NUMERIC, ForeignKey, Integer, inspect
# deklaracja funkcji do pobierania uzytkownika po jego id unique=True

@login_manager.user_loader
def load_user(user_id):
    return uzytkownicy.query.get(int(user_id))

class Kontrahenci(db.Model):
    _tablename_ = "kontrahenci"
    id_kon = db.Column(db.Integer, primary_key=True)
    NIP = db.Column(db.String(20))
    nazwa_firmy = db.Column(db.String(20), nullable=False)
    miasto = db.Column(db.String(50), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    ulica = db.Column(db.String(32), nullable=False)
    numer = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    stan = db.Column(db.String(32), nullable=False)
    #Typ_dostawcy = db.Column(db.String(32), nullable=False) !!!!!
    #NIP - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli dokumenty przez Kontrahenta. Krotke NIP.
    dokumenty = db.relationship('dokumenty', backref='kontrahent')

    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<nazwa_firmy('%s'), NIP('%s')>" % (self.nazwa_firmy, self.NIP)
 
class dokumenty(db.Model):
    _tablename_ = "dokumenty"
    id_dokumentu = db.Column(db.Integer, primary_key=True)
    numer_dokumentu = db.Column(db.String(20), nullable=False, unique=True)
    magazyn_towary = db.relationship("MagazynTowar", backref='dokument')
    data_wystawienia = db.Column(db.Date, nullable=False)
    id_uzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
    imie_uzytkownika = db.Column(db.String(20))
    id_kon = db.Column(db.Integer, db.ForeignKey('kontrahenci.id_kon'))
    typ_dokumentu = db.Column(db.String(32), nullable=False)
    data_przyjecia = db.Column(db.Date)
    statusd = db.Column(db.String(20), nullable=False)
    towaryy = db.relationship("TowaryDokument", backref='dokument')
    
    def __init__(self, numer_dokumentu):
        self.numer_dokumentu = numer_dokumentu

        
    #def __repr__(self):
    #    return "<Numer_dokumentu('%s'), data_wystawienia(%s)>" % (self.numer_dokumentu, self.data_wystawienia)


class uzytkownicy(db.Model, UserMixin):
    _tablename_ = "uzytkownicy"
    #id - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli dokumenty przez Uzytkownicy.
    id = db.Column(db.Integer, primary_key=True, unique=True)
    imie = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    haslo = db.Column(db.VARCHAR(100), nullable=False)
    typ = db.Column(db.String(30), nullable=False)  
    stan = db.Column(db.String(30), nullable=False)  
    dokumenty_relacja = db.relationship('dokumenty', backref='uzytkownicy')

    #funkcja wypisująca określone elementy. Elementy które są wypisywane pojawiają się po "self"
    def __repr__(self):
        return "<email('%s'), typ/stanowisko('%s'), imie('%s')>" % (self.email, self.typ, self.imie)

   

class TowaryDokument(db.Model):
    _tablename_ = "towary_dokument"
    id = db.Column(db.Integer, primary_key=True)
    numer_towaru = db.Column(db.Integer)
    id_dokumentu = db.Column(db.String(20), db.ForeignKey('dokumenty.numer_dokumentu'))
    id_towaru = db.Column(db.Integer, db.ForeignKey('towary.id_towaru'))
    ilosc = db.Column(db.Integer, nullable=False)
    data_przyjecia = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"<TowaryDokument id:{self.id}, id_dokumentu:{self.id_dokumentu}, id_towaru:{self.id_towaru}, ilosc:{self.ilosc}, data_waznosci:{self.data_waznosci}>"

class Towary(db.Model):
    _tablename_ = "towary"

    NIP = db.Column(db.String(20), nullable=False)
    id_towaru = db.Column(db.Integer, primary_key=True)
    dokumenty = db.relationship('TowaryDokument', backref='towary')
    typ = db.Column(db.String(32), nullable=False)
    rodzaj = db.Column(db.String(32), nullable=False)
    nazwa = db.Column(db.String(32), nullable=False)
    stan = db.Column(db.String(32), nullable=False)
    magazyn_towar_rel = db.relationship("MagazynTowar", backref='towar')

class Sekcja(db.Model):
    _tablename_ = "sekcja"
    #nr_sekcji - relacja jeden do wielu. Nadanie uprawnień do wszystkich atrybutów w tabeli magazyn_towar przez Magazyn.
    nr_sekcji = db.Column(db.String(32), primary_key=True)
    pojemnosc_sekcji = db.Column(db.Integer, nullable=False)
    towary = db.relationship('MagazynTowar', backref='sekcja')

class MagazynTowar(db.Model):
    _tablename_ = "magazyn_towar"
    idmag = db.Column(db.Integer, primary_key=True)
    nr_sekcji = db.Column(db.String(32), db.ForeignKey('sekcja.nr_sekcji'))
    data_przyjecia=db.Column(db.Date, nullable=False)
    id_towaru=db.Column(db.Integer, db.ForeignKey('towary.id_towaru'))
    numer_dokumentu = db.Column(db.String(20), db.ForeignKey('dokumenty.numer_dokumentu'))
    stan = db.Column(db.String(20))

