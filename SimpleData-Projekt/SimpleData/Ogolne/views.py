from flask import Blueprint, jsonify, render_template, url_for, redirect
from datetime import datetime
ogolne = Blueprint('ogolne', __name__)
from flask_login import current_user, login_required, logout_user
from SimpleData import  db, bcrypt, app

from SimpleData.Ogolne.forms import przeszukiwanie_d
from sqlalchemy import inspect, text
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from SimpleData.tabele import uzytkownicy



@ogolne.route('/api/time') # ustawiamy ścieżkę po jakiej będzie można się dostać do danej wartości/strony po wpisaniu w przeglądarkę
def current_time():
    now = datetime.now()  #pobieramy obecny czas z systemu
    formatted_now = now.strftime("%A, %d %B, %Y %H:%M") #ustalamy w jakim formacie będzie wyświetlany czas
    return jsonify({'time': formatted_now})

@ogolne.route('/')
@ogolne.route('/home') #Aby dana strona była dostępna pod dwoma ścieżkami wystarczy dodać pod sobą dwie linie kodu @app.route
def home():
    user = current_user.imie if current_user.is_authenticated else None
    return render_template( #używamy render_teamplate aby wygenerować stronę z danego pliku html, tworząc zmienne możemy je przekazać na stronę i następnie je tam wywołać
        "home.html",
        title = "SimpleData",    #taka zmienna którą możemy wyświetlić na stronie
        user=user
    )

@ogolne.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("ogolne.home"))

@ogolne.route('/przeszukiwanie', methods=['GET', 'POST'])
@login_required
def przeszukiwanie():
    form = przeszukiwanie_d()
    return render_template(
        "przeszukiwanie.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form
    )

