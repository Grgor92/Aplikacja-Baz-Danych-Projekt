from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField #importujemy odpowiednie elemnety aby móc sprawdzić poprawność formularza
from wtforms.validators import Optional

class magazyn_towar(FlaskForm):
    idm = IntegerField('id', validators=[Optional()])
    nr_sekcji = StringField('Numer sekcji', validators=[Optional()])
    data_przyjecia = DateField('data przyjęcia', validators=[Optional()])
    id_towaru = IntegerField('Id towaru', validators=[Optional()])
    numer_dokumentu = StringField('numer dokumentu', validators=[Optional()])
    submit = SubmitField('Wyszukaj')
    