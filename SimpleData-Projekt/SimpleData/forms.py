from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField #importujemy odpowiednie elemnety aby móc sprawdzić poprawnośc formularza
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):  #tworzymy klasę o odppowiedniej nazwie
    Nazwa = StringField('Nazwa', validators=[DataRequired(), Length(min=6, max=20)])    #tworzymy pola i definjujemy typ zmiennej, oraz dodajemy poprawno�ci jakie ma zawiera pole
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Haslo', validators=[DataRequired(),Length(min=6, max=32)])
    haslo2 = PasswordField('Potwierdz Haslo', validators=[DataRequired(),EqualTo('haslo'),Length(min=6, max=32)])

    submit = SubmitField('Zarejestruj')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Haslo', validators=[DataRequired(),])
    submit = SubmitField('Zaloguj')

