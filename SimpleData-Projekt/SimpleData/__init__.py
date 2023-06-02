# -*- coding: utf-8 -*-
#Import biblioteki
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
#Bibloteka odpowiedzialna za bezpieczne haszowanie haseł
from flask_bcrypt import Bcrypt
from flask import Flask, session, redirect, url_for, flash
from functools import wraps
from flask_login import current_user
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)

# generowanie klucza losowego
SECRET_KEY = os.urandom(32)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.sesion = True
@login_manager.unauthorized_handler
def unauthorized():
    flash('Musisz się zalogować, aby uzyskać dostęp do tej strony!', 'danger')
    return redirect(url_for('ogolne.home'))

@login_manager.needs_refresh_handler
def needs_refresh():
    flash('Twoja sesja wygasła, zaloguj się ponownie!', 'danger')
    return redirect(url_for('ogolne.logout'))

# ustawienie klucza w konfiguracji aplikacji
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=60)
@app.before_first_request
def init_session():
    session.permanent = True

#Łączenie z bazą danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql7622214:aFWewSyz9l@sql7.freesqldatabase.com/sql7622214'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#mysql://sql7622214:aFWewSyz9l@sql7.freesqldatabase.com/sql7622214
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)



def roles_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if not any(role == current_user.typ for role in roles):
                flash('Nie masz uprawnień do tej strony!', 'danger')
                return redirect(url_for('ogolne.home'))

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


from SimpleData.Dokumenty.views import dok
from SimpleData.Kontrahenci.views import kon
from SimpleData.Ogolne.views import ogolne
from SimpleData.Towary.views import tow
from SimpleData.Uzytkownicy.views import users
from SimpleData.Magazyn.views import mag

app.register_blueprint(dok)
app.register_blueprint(kon)
app.register_blueprint(ogolne)
app.register_blueprint(tow)
app.register_blueprint(users)
app.register_blueprint(mag)
