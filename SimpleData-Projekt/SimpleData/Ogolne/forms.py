from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from SimpleData.tabele import uzytkownicy, Kontrahenci, dokumenty
from datetime import date

class przeszukiwanie_d(FlaskForm):
    rodzaj = SelectField('Dokument', choices=[('WZ', 'WZ'), ('PZ', 'PZ')])
    numer = IntegerField('Numer')
    data_od = DateField('Data od')
    data_do = DateField('Data do')
    kontrahent = SelectField('Kontarhent: ', choices=[('muszynianka', 'Muszynianka'), ('galicjanka', 'Galicjanka')])
    submit = SubmitField('Wyszukaj')

class dok_historyczne(FlaskForm):
    numer_dok = IntegerField('Numer dokumentu', validators = [Optional()])
    data_wys = DateField('Data wystawienia', validators = [Optional()])
    id_klienta = IntegerField('Id klienta', validators = [Optional()])
    nip = IntegerField('NIP', validators = [Optional()])
    rodzaj = SelectField('Dokument', choices=[('', ''),('WZ', 'WZ'), ('PZ', 'PZ')], validators = [Optional()])
    data_wyk = DateField('Data wykonania', validators = [Optional()])
    nazwa_kon = QuerySelectField('Kontrahent', query_factory=lambda: kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
    submit = SubmitField('Wyszukaj')
