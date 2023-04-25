from flask_wtf import FlaskForm
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
