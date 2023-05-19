from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty
from datetime import date

class DodajDokumentForm(FlaskForm):
    numer_dok2 = IntegerField('Numer dokumentu', validators=[DataRequired()])
    data_wys2 = DateField('Data wystawienia', default=date.today(), validators=[DataRequired()], render_kw={'readonly': True})
    nip2 = IntegerField('NIP', validators=[DataRequired()])
    kontrahent2 = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[DataRequired()])
    rodzaj2 = SelectField('Rodzaj dokumentu', choices=[('WZ', 'WZ'), ('PZ', 'PZ')], validators=[DataRequired()], render_kw={'disabled': True})
    data_wyk2 = DateField('Data wykonania', validators=[Optional()])
    data_waz2 = DateField('Data Waznosci towaru ', validators=[DataRequired()])
    status = SelectField('Status dokumentu', choices=[('Edycja', 'Edycja'), ('Aktywna', 'Aktywna')], validators=[Optional()])
    submit2 = SubmitField('Dodaj dokument')

    def validate_numer_dok2(self, numer_dok2):
        Uzyt = Dokumenty.query.filter_by(numer_dokumentu=numer_dok2.data).first()
        if Uzyt:
            raise ValidationError('Dokuemnt o takim numerze już istnieje.')

    #def validate(self, numer_dok2):
    #    existing_doc = Dokumenty.query.filter_by(numer_dokumentu=self.numer_dok2.data).first()
    #    if existing_doc:
    #        raise ValidationError('Ta nazwa użytkownika już istnieje. Wybierz inną nazwę.')

    #    if not self.id_klienta.data and not self.nip.data:
    #        self.id_klienta.errors.append('Podaj numer klienta lub NIP.')
    #        self.nip.errors.append('Podaj numer klienta lub NIP.')
    #        return False

    #    return True
class dok_historyczne(FlaskForm):
    numer_dok = IntegerField('Numer dokumentu', validators = [Optional()])
    data_wys = DateField('Data wystawienia', validators = [Optional()])
    id_klienta = IntegerField('Id klienta', validators = [Optional()])
    nip = IntegerField('NIP', validators = [Optional()])
    rodzaj = SelectField('Dokument', choices=[('', ''),('WZ', 'WZ'), ('PZ', 'PZ')], validators = [Optional()])
    data_wyk = DateField('Data wykonania', validators = [Optional()])
    nazwa_kon = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
    submit = SubmitField('Wyszukaj')

