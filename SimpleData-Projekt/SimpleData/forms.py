from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):  #tworzymy klasę o odppowiedniej nazwie
    Nazwa = StringField('Nazwa', validators=[DataRequired(), Length(min=6, max=20)])    #tworzymy pola i definjujemy typ zmiennej, oraz dodajemy poprawności jakie ma zawierać pole
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Haslo', validators=[DataRequired(),Length(min=6, max=32)])
    haslo2 = PasswordField('Potwierdz Haslo', validators=[DataRequired(),EqualTo('haslo'),Length(min=6, max=32)])
    typ_uzytkownika = SelectField('Typ użytkownika', choices=[('', 'Wybierz typ'), ('administrator', 'Administrator'), ('kierownik', 'Kierownik'), ('pracownik', 'Pracownik')], validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')

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
    numer_dok = IntegerField('Numer dokumentu')
    data_wys = DateField('Data wystawienia')
    id_klienta = IntegerField('Id klienta')
    nip = IntegerField('NIP')
    rodzaj = SelectField('Dokument', choices=[('WZ', 'WZ'), ('PZ', 'PZ')])
    data_wyk = DateField('Data wykonania')
    submit = SubmitField('Wyszukaj')

class kontrahenci(FlaskForm):
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
    typ = SelectField('Typ', choices=[('', 'Wybierz typ'), ('adm', 'Administrator'), ('ki', 'Kierownik'), ('pr', 'Pracownik')])
    submit = SubmitField('Wyszukaj')

class magazyn_towar(FlaskForm):
    nr_sekcji = StringField('Numer sekcji')
    id_towaru = IntegerField('Id towaru')
    submit = SubmitField('Wyszukaj')

#class ustawienia(db.Model, UserMixin):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(64), index=True, unique=True)
#    password_hash = db.Column(db.String(128))
    
#    def ustaw_haslo(self, password):
#        self.password_hash = generate_password_hash(password)
        
#    def sprawdz_haslo(self, password):
#        return check_password_hash(self.password_hash, password)
