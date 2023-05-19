from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from .tabele import Uzytkownicy, Kontrahenci, Dokumenty
from datetime import date








    
    #def validate_email(self, email):
    #    user = Uzytkownicy.query.filter_by(email=email.data).first()
    #    if user and user.id != self.id.data:
    #        raise ValidationError('Ten adres email jest już w użyciu.')




#class Dodaj_dok(FlaskForm):
#    numer_dok = IntegerField('Numer dokumentu', validators = [Optional()])
#    data_wys = DateField('Data wystawienia', validators = [Optional()])
#    id_klienta = IntegerField('Id klienta', validators = [Optional()])
#    nip = IntegerField('NIP', validators = [Optional()])
#    rodzaj = SelectField('Dokument', choices=[('', ''),('WZ', 'WZ'), ('PZ', 'PZ')], validators = [Optional()])
#    data_wyk = DateField('Data wykonania', validators = [Optional()])
#    nazwa_kon = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
#    submit = SubmitField('Wyszukaj')



