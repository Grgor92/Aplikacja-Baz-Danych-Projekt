from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza


class magazyn_towar(FlaskForm):
    id = IntegerField('id')
    nr_sekcji = StringField('Numer sekcji')
    data_przyjecia = DateField('data przyjęcia')
    id_towaru = IntegerField('Id towaru')
    numer_dokumentu = StringField('numer dokumentu')

    submit = SubmitField('Wyszukaj')
    