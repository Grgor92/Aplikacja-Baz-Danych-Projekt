from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza

class kontrahenci_F(FlaskForm):
    nip = StringField('NIP')
    nazwa_firmy = StringField('Nazwa firmy')
    miasto = StringField('Miasto')
    nr_telefonu = IntegerField('Telefon')
    ulica = StringField('Ulica')
    numer = IntegerField('Numer')
    rodzaj = StringField('Rodzaj')
    submit = SubmitField('Wyszukaj')
