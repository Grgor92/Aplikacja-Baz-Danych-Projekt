from flask_wtf import FlaskForm
from sqlalchemy import text
from SimpleData import db
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, ValidationError, Optional, NumberRange
from SimpleData.tabele import Kontrahenci, dokumenty
from datetime import date

class DodajDokumentForm(FlaskForm):
    numer_dok2 = IntegerField('Numer dokumentu', validators=[DataRequired()])
    data_wys2 = DateField('Data wystawienia', default=date.today(), validators=[DataRequired()], render_kw={'readonly': True})
    nip2 = StringField('NIP', validators=[DataRequired()])
    rodzaj2 = SelectField('Rodzaj dokumentu', choices=[('WZ', 'WZ'), ('PZ', 'PZ')], validators=[DataRequired()])

    # QuerySelectField To pole kóre pozwla na wybranie danych z bazy i wyświetlenie ich w polsu formularza select
    kontrahentWZ = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.filter_by(status='Odbiorca', stan="Aktywny").all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
    kontrahentPZ = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.filter_by(status='Dostawca', stan="Aktywny").all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])

    status = SelectField('Status dokumentu', choices=[('Edycja', 'Edycja'), ('Aktywna', 'Aktywna')], validators=[Optional()])
    submit2 = SubmitField('Dodaj dokument')

    #Ustawiamy własną walidację na pola formularza
    def validate_kontrahent(self, kontrahent):
        nip = self.nip2.data
        query = text("SELECT * FROM kontrahenci WHERE NIP = :nip AND nazwa_firmy = :kontrahent")
        result = db.session.execute(query, {'nip': nip, 'kontrahent': kontrahent}).fetchone()
        if not result:
            raise ValidationError('Podany NIP i kontrahent nie pasują do siebie.')

    def validate_kontrahentWZ(self, kontrahentWZ):
        if self.kontrahentWZ.data and self.rodzaj2.data == 'WZ':
            self.validate_kontrahent(kontrahentWZ.data.nazwa_firmy)

    def validate_kontrahentPZ(self, kontrahentPZ):
        if self.kontrahentPZ.data and self.rodzaj2.data == 'PZ':
            self.validate_kontrahent(kontrahentPZ.data.nazwa_firmy)

    def validate_numer_dok2(self, numer_dok2):
        dokument = dokumenty.query.filter_by(numer_dokumentu=numer_dok2.data).first()
        if dokument:
            raise ValidationError('Dokument o takim numerze już istnieje.')

class Dok(FlaskForm):
    numer_dokumentu = IntegerField('Numer dokumentu', validators=[Optional()])
    data_wystawienia = DateField('Data wystawienia', validators=[Optional()])
    id_uzytkownika = IntegerField('Id użytkownika', validators=[Optional()])
    id_kon = IntegerField('NIP kontrahenta', validators=[Optional()])
    typ_dokumentu = SelectField('Typ dokumentu', choices=[('', ''), ('WZ', 'WZ'), ('PZ', 'PZ')], validators=[Optional()])
    data_przyjecia = DateField('Data Wykonania', validators=[Optional()])
    statusd = SelectField('Status dokumentu', choices=[('Aktywna', 'Aktywna'),('', '') ,('Edycja', 'Edycja'), ('Zakończona', 'Zakończona')], validators=[Optional()])
    submit = SubmitField('Wyszukaj')

class DodajTowarDokument(FlaskForm):
    id_towaru = IntegerField('Numer towaru', validators = [Optional()])
    numer_magazynu = IntegerField('Numer Towaru', validators = [Optional()])
    typ = StringField('Data wystawienia', validators = [Optional()])
    rodzaj= StringField('Rodzaj Wody', validators = [Optional()])
    nazwa= StringField('Nazwa Wody', validators = [Optional()])
    il= IntegerField('Ilosc', validators = [DataRequired(), NumberRange(min=0)])
    il_mag= IntegerField('Ilosc', validators = [Optional(), NumberRange(min=0)])
    submit = SubmitField('Dodaj Towar')

