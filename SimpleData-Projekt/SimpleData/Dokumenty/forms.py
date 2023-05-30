from flask_wtf import FlaskForm
from sqlalchemy import text
from SimpleData import db
from flask import request
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, ValidationError, Optional, NumberRange
from SimpleData.tabele import Kontrahenci, dokumenty
from datetime import date


class DodajDokumentForm(FlaskForm):
    numer_dok2 = IntegerField('Numer dokumentu', validators=[DataRequired()])
    data_wys2 = DateField('Data wystawienia', default=date.today(), validators=[DataRequired()], render_kw={'readonly': True})
    nip2 = IntegerField('NIP', validators=[DataRequired()])
    rodzaj2 = SelectField('Rodzaj dokumentu', choices=[('WZ', 'WZ'), ('PZ', 'PZ')], validators=[DataRequired()])
    kontrahentWZ = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.filter_by(status='Odbiorca').all(), get_label='nazwa_firmy', allow_blank=True, validators=[DataRequired()])
    kontrahentPZ = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.filter_by(status='Dostawca').all(), get_label='nazwa_firmy', allow_blank=True, validators=[DataRequired()])
    data_wyk2 = DateField('Data wykonania', validators=[Optional()])
    data_waz2 = DateField('Data Waznosci towaru', validators=[DataRequired()])
    status = SelectField('Status dokumentu', choices=[('Edycja', 'Edycja'), ('Aktywna', 'Aktywna')], validators=[Optional()])
    submit2 = SubmitField('Dodaj dokument')

    def validate(self):
        if not super().validate():
            return False
        nip = self.nip2.data
        kontrahent = self.kontrahent2.data.nazwa_firmy
        query = text("SELECT * FROM kontrahenci WHERE NIP = :nip AND nazwa_firmy = :kontrahent")
        result = db.session.execute(query, {'nip': nip, 'kontrahent': kontrahent}).fetchone()
        if not result:
            self.nip2.errors.append('Podany NIP i kontrahent nie pasują do siebie.')
            self.kontrahent2.errors.append('Podany NIP i kontrahent nie pasują do siebie.')
            return False

        return True

    def validate_numer_dok2(self, numer_dok2):
        dokument = dokumenty.query.filter_by(numer_dokumentu=numer_dok2.data).first()
        if dokument:
            raise ValidationError('Dokument o takim numerze już istnieje.')


    #def validate_nip2(self, nip2):
    #    nip = nip2.data
    #    kontrahent = self.kontrahent2.data
    #    query = text("SELECT * FROM kontrahenci WHERE NIP = :nip AND nazwa_firmy = :kontrahent")
    #    result = db.session.execute(query, {'nip': nip, 'kontrahent': kontrahent}).fetchone()
    #    if not result:
    #        raise ValidationError('Podany NIP i kontrahent nie pasują do siebie.')

    #def validate(self, numer_dok2):
    #    existing_doc = Dokumenty.query.filter_by(numer_dokumentu=self.numer_dok2.data).first()
    #    if existing_doc:
    #        raise ValidationError('Ta nazwa użytkownika już istnieje. Wybierz inną nazwę.')

    #    if not self.id_klienta.data and not self.nip.data:
    #        self.id_klienta.errors.append('Podaj numer klienta lub NIP.')
    #        self.nip.errors.append('Podaj numer klienta lub NIP.')
    #        return False

    #    return True
    #def validate_nip2(self, nip2):
    #    kontrahent = self.kontrahent2.data
    #    uzytkownik = kontrahenci.query.filter_by(NIP=nip2.data).first()
    #    if uzytkownik: 
    #        if uzytkownik.nazwa_firmy != kontrahent:
    #            raise ValidationError('Podany NIP i kontrahent nie pasują do siebie.')
    
    #def validate_kontrahent2(self, kontrahent2):
    #    nip = self.nip2.data
    #    uzytkownik = kontrahenci.query.filter_by(nazwa_firmy=str(kontrahent2.data)).first()
    #    if uzytkownik: 
    #        if uzytkownik.NIP != nip:
    #            raise ValidationError('Podany NIP i kontrahent nie pasują do siebie.')
class dok_historyczne(FlaskForm):
    numer_dokumentu = IntegerField('Numer dokumentu', validators=[Optional()])
    data_wystawienia = DateField('Data wystawienia', validators=[Optional()])
    id_uzytkownika = IntegerField('Id użytkownika', validators=[Optional()])
    NIP_kontrahenta = IntegerField('NIP kontrahenta', validators=[Optional()])
    typ_dokumentu = SelectField('Typ dokumentu', choices=[('', ''), ('WZ', 'WZ'), ('PZ', 'PZ')], validators=[Optional()])
    data_wykonania = DateField('Data wykonania', validators=[Optional()])
    statusd = SelectField('Status dokumentu', choices=[('', '') ,('Aktywna', 'Aktywna'), ('Edycja', 'Edycja')], validators=[Optional()])
    submit = SubmitField('Wyszukaj')

    
    #def validate_email(self, email):
    #    user = Uzytkownicy.query.filter_by(email=email.data).first()
    #    if user and user.id != self.id.data:
    #        raise ValidationError('Ten adres email jest już w użyciu.')


class DodajTowarDokument(FlaskForm):
    id_towaru = IntegerField('Numer towaru', validators = [DataRequired()])
    typ = StringField('Data wystawienia', validators = [DataRequired()])
    rodzaj= StringField('Rodzaj Wody', validators = [DataRequired()])
    nazwa= StringField('Nazwa Wody', validators = [DataRequired()])
    il= IntegerField('Ilosc', validators = [DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Dodaj Towar')
    #id_towaru = db.Column(db.Integer, primary_key=True)
    #typ = db.Column(db.String(32), nullable=False)
    #rodzaj = db.Column(db.String(32), nullable=False)
    #nazwa = db.Column(db.String(32), nullable=False)
#class Dodaj_dok(FlaskForm):
#    numer_dok = IntegerField('Numer dokumentu', validators = [Optional()])
#    data_wys = DateField('Data wystawienia', validators = [Optional()])
#    id_klienta = IntegerField('Id klienta', validators = [Optional()])
#    nip = IntegerField('NIP', validators = [Optional()])
#    rodzaj = SelectField('Dokument', choices=[('', ''),('WZ', 'WZ'), ('PZ', 'PZ')], validators = [Optional()])
#    data_wyk = DateField('Data wykonania', validators = [Optional()])
#    nazwa_kon = QuerySelectField('Kontrahent', query_factory=lambda: kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
#    submit = SubmitField('Wyszukaj')

