from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from .tabele import Uzytkownicy, Kontrahenci, Dokumenty
from datetime import date

class RegistrationForm(FlaskForm):  #tworzymy klasę o odppowiedniej nazwie
    Nazwa = StringField('Nazwa', validators=[DataRequired(), Length(min=5, max=20)])    #tworzymy pola i definjujemy typ zmiennej, oraz dodajemy poprawności jakie ma zawierać pole
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Haslo', validators=[DataRequired(),Length(min=5, max=32)])
    haslo2 = PasswordField('Potwierdz Haslo', validators=[DataRequired(),EqualTo('haslo'),Length(min=5, max=32)])
    typ_uzytkownika = SelectField('Typ użytkownika', choices=[('', 'Wybierz typ'), ('administrator', 'Administrator'), ('kierownik', 'Kierownik'), ('pracownik', 'Pracownik')], validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')
    def validate_Nazwa(self, Nazwa):
        Uzyt = Uzytkownicy.query.filter_by(imie=Nazwa.data).first()
        if Uzyt:
            raise ValidationError('Ta nazwa użytkownika już istnieje. Wybierz inną nazwę.')
    #
    def validate_email(self, email):
        Uzyt = Uzytkownicy.query.filter_by(email=email.data).first()
        if Uzyt:
            raise ValidationError('Ten email już istnieje. Wybierz inną nazwę.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Haslo', validators=[DataRequired(),])
    submit = SubmitField('Zaloguj')

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
    nazwa_kon = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
    submit = SubmitField('Wyszukaj')

class kontrahenci_F(FlaskForm):
    nip = IntegerField('NIP')
    nazwa_firmy = StringField('Nazwa firmy')
    miasto = StringField('Miasto')
    nr_telefonu = IntegerField('Telefon')
    ulica = StringField('Ulica')
    numer = IntegerField('Numer')
    submit = SubmitField('Wyszukaj')

class uzytkownicy(FlaskForm):
    imie = StringField('Imie')
    email = StringField('Email')
    haslo = StringField('Hasło')
    typ = SelectField('Typ', choices=[('', 'Wybierz typ'), ('Administrator', 'Administrator'), ('Kierownik', 'Kierownik'), ('Pracownik', 'Pracownik')])
    submit = SubmitField('Wyszukaj')

    
class Users_zmiana(FlaskForm):
    imie = StringField('Imie', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    uprawnienia = SelectField('Typ', choices=[('', 'Wybierz typ'), ('Administrator', 'Administrator'), ('Kierownik', 'Kierownik'), ('Pracownik', 'Pracownik')], validators=[DataRequired()])
    submit = SubmitField('Zapisz zmiany')
    
    #def validate_email(self, email):
    #    user = Uzytkownicy.query.filter_by(email=email.data).first()
    #    if user and user.id != self.id.data:
    #        raise ValidationError('Ten adres email jest już w użyciu.')

class magazyn_towar(FlaskForm):
    nr_sekcji = StringField('Numer sekcji')
    id_towaru = IntegerField('Id towaru')
    submit = SubmitField('Wyszukaj')
    
class moje_ustawienia(FlaskForm):
    username = StringField('Nazwa', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Stare hasło', validators=[DataRequired()])
    new_password = PasswordField('Nowe hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Zapisz')

#class Dodaj_dok(FlaskForm):
#    numer_dok = IntegerField('Numer dokumentu', validators = [Optional()])
#    data_wys = DateField('Data wystawienia', validators = [Optional()])
#    id_klienta = IntegerField('Id klienta', validators = [Optional()])
#    nip = IntegerField('NIP', validators = [Optional()])
#    rodzaj = SelectField('Dokument', choices=[('', ''),('WZ', 'WZ'), ('PZ', 'PZ')], validators = [Optional()])
#    data_wyk = DateField('Data wykonania', validators = [Optional()])
#    nazwa_kon = QuerySelectField('Kontrahent', query_factory=lambda: Kontrahenci.query.all(), get_label='nazwa_firmy', allow_blank=True, validators=[Optional()])
#    submit = SubmitField('Wyszukaj')

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


