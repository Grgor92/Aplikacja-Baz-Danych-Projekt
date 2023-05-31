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


class magazyn_towar(FlaskForm):
    nr_sekcji = StringField('Numer sekcji')
    id_towaru = IntegerField('Id towaru')
    submit = SubmitField('Wyszukaj')
    
