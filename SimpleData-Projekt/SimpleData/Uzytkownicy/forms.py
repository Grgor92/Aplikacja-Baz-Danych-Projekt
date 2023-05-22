from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty
from datetime import date

class RegistrationForm(FlaskForm):  #tworzymy klasę o odppowiedniej nazwie
    Nazwa = StringField('Nazwa', validators=[DataRequired(), Length(min=5, max=20)])    #tworzymy pola i definjujemy typ zmiennej, oraz dodajemy poprawności jakie ma zawierać pole
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Haslo', validators=[DataRequired(),Length(min=5, max=32)])
    haslo2 = PasswordField('Potwierdz Haslo', validators=[DataRequired(),EqualTo('haslo'),Length(min=5, max=32)])
    typ_uzytkownika = SelectField('Typ użytkownika', choices=[('', 'Wybierz typ'), ('Administrator', 'Administrator'), ('Kierownik', 'Kierownik'), ('Pracownik', 'Pracownik')], validators=[DataRequired()])
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

class moje_ustawienia(FlaskForm):
    username = StringField('Nazwa', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Stare hasło', validators=[DataRequired()])
    new_password = PasswordField('Nowe hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Zapisz')

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
