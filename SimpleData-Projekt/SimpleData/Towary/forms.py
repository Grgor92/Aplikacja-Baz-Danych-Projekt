from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from SimpleData.tabele import uzytkownicy, kontrahenci, dokumenty
from datetime import date

class DodajDokumentForm(FlaskForm):
    numer_dok2 = IntegerField('Numer dokumentu', validators=[DataRequired()])
    data_wys2 = DateField('Data wystawienia', default=date.today(), validators=[DataRequired()], render_kw={'readonly': True})
    nip2 = IntegerField('NIP', validators=[DataRequired()])
    kontrahent2 = QuerySelectField('Kontrahent', query_factory=lambda: kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[DataRequired()])
    rodzaj2 = SelectField('Rodzaj dokumentu', choices=[('WZ', 'WZ'), ('PZ', 'PZ')], validators=[DataRequired()], render_kw={'disabled': True})
    data_wyk2 = DateField('Data wykonania', validators=[Optional()])
    data_waz2 = DateField('Data Waznosci towaru ', validators=[DataRequired()])
    status = SelectField('Status dokumentu', choices=[('Edycja', 'Edycja'), ('Aktywna', 'Aktywna')], validators=[Optional()])
    submit2 = SubmitField('Dodaj dokument')

    def validate_numer_dok2(self, numer_dok2):
        Uzyt = dokumenty.query.filter_by(numer_dokumentu=numer_dok2.data).first()
        if Uzyt:
            raise ValidationError('Dokuemnt o takim numerze już istnieje.')
