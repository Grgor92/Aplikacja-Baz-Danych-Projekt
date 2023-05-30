from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from SimpleData.tabele import uzytkownicy, Kontrahenci, dokumenty
from datetime import date


class magazyn_towar(FlaskForm):
    id = IntegerField('id')
    nr_sekcji = StringField('Numer sekcji')
    data_przyjęcia = DateField('data przyjęcia')
    id_towaru = IntegerField('Id towaru')
    numer_dokumentu = StringField('numer dokumentu')

    submit = SubmitField('Wyszukaj')
    