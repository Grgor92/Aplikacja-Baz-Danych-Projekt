# -*- coding: utf-8 -*-
from enum import Flag
from flask import render_template, jsonify, redirect, url_for, flash, session
from SimpleData import app
from datetime import datetime
from .forms import RegistrationForm, LoginForm, przeszukiwanie_d, dok_historyczne, kontrahenci, uzytkownicy, magazyn_towar # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db
from .tabele import Users
from sqlalchemy import inspect

#wewnątrz aplikacji 
with app.app_context():
#sprawdzenie czy tabela istnieje
    inspector = inspect(db.engine)
    db.drop_all()
    if not inspector.has_table('Users'):
        db.create_all()
    new_product = Users(nazwa='admin', email='sd@admin.com', haslo='haslo', uprawnienia='Kierownik')
    db.session.add(new_product)
    db.session.commit()
        

@app.route('/api/time', ) # ustawiamy ścieżkę po jakiej będzie można się dostać do danej wartości/strony po wpisaniu w przeglądarkę
def current_time():
    now = datetime.now()  #pobieramy obecny czas z systemu
    formatted_now = now.strftime("%A, %d %B, %Y %H:%M") #ustalamy w jakim formacie będzie wyświetlany czas
    return jsonify({'time': formatted_now})

@app.route('/')
@app.route('/home') #Aby dana strona była dostępna pod dwoma ścieżkami wystarczy dodać pod sobą dwie linie kodu @app.route
def home():
    user = session.get('user', None) # pobieramy wartość z sesji lub ustawiamy na None, jeśli nie istnieje
    return render_template( #używamy render_teamplate aby wygenerować stronę z danego pliku html, tworząc zmienne możemy je przekazać na stronę i następnie je tam wywołać
        "home.html",
        title = "SimpleData",    #taka zmienna którą możemy wyświetlić na stronie
        ur = user
    )
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/login',methods=['GET', 'POST'])    #oprócz ścieżki dodajemmy tu metody jakie mogą być obsługiwane na stronie, w tym momencie robimy to aby ta strona mogła onsługiwać formularze
def login():
    form = LoginForm()  #do zmiennej form przypisujemy model formularza który będzie działał na tej stronie
    user = session.get('user', None)
    if form.validate_on_submit():   
        if form.email.data == 'admin@sd.com' and form.haslo.data == 'haslo':    #dal potrzeby sprawdzenia walidacji danych ustawione jest sztywne email i hasło po któym będzie się można zalogować
            flash('Udało się zalogować', 'success') #wiadomość która ma się pokazać po porawnym wpisaniu danych
            user = form.email.data
            session['user'] = user
            return redirect(url_for('home'))
        else:
            user = session.get('user', None)
            flash('Logowanie nie udane. Sprawdź poprawność danych a wrazie dalszych problemów skontaktuj się z administratorem', 'danger')  #wiadomość jeśli dane będą nie poprawne
    return render_template(
        "login.html",
        title = "Logowanie",
        ur = user,
        form=form #rendereujemy stronę i przekzaujemy formularz
        )
@app.route('/rejestruj', methods=['GET', 'POST'])
def rejestr():
    user = session.get('user', None)
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.Nazwa.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('rejestr.html', 
        title='Rejestracja',
        ur = user,
        form=form
        )
@app.route('/przeszukiwanie', methods=['GET', 'POST'])
def przeszukiwanie():
    form = przeszukiwanie_d()
    user = session.get('user', None)
    return render_template(
        "przeszukiwanie.html",
        title = "SimpleData",
        ur = user,
        form=form
    )
@app.route('/dokumenty_historyczne', methods=['GET', 'POST'])
def dokumenty_hist():
    form = dok_historyczne()
    user = session.get('user', None)
    return render_template(
        "dokumenty_historyczne.html",
        title = "SimpleData",
        ur = user,
        form=form
    )

@app.route('/kontrahenci', methods=['GET', 'POST'])
def kontrahenci_t():
    form = kontrahenci()
    user = session.get('user', None)
    return render_template(
        "kontrahenci.html",
        title = "SimpleData",
        ur = user,
        form=form
    )

@app.route('/uzytkownicy', methods=['GET', 'POST'])
def uzytkownicy_t():
    form = uzytkownicy()
    user = session.get('user', None)
    return render_template(
        "uzytkownicy.html",
        title = "SimpleData",
        ur = user,
        form=form
    )

@app.route('/magazyn_towar', methods=['GET', 'POST'])
def magazyn_towar_t():
    form = magazyn_towar()
    user = session.get('user', None)
    return render_template(
        "magazyn_towar.html",
        title = "SimpleData",
        ur = user,
        form=form
    )