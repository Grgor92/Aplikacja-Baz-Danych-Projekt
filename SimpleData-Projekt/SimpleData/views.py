# -*- coding: utf-8 -*-

from enum import Flag
from flask import render_template, jsonify, redirect, url_for
from SimpleData import app
from flask import flash
from datetime import datetime
from .forms import RegistrationForm, LoginForm # import z inego plaiku w tym samym miejscu musi zawirać . przed nazwą


@app.route('/api/time', ) # ustawiamy ścierzkę po jakiej będzie można się dostać do danej wartości/strony po wpisaniu w przeglądarkę
def current_time():
    now = datetime.now()  #pobieramy obecny czas z systemu
    formatted_now = now.strftime("%A, %d %B, %Y %H:%M") #ustalamy w jakim formacie będzie wyświetlany czas
    return jsonify({'time': formatted_now})

@app.route('/')
@app.route('/home') #Aby dana strona była dostępna pod dwoma ścierzkami wystarczy dodać pod sobą dwie linie kodu @app.route
def home():
    return render_template( #używamy render_teamplate aby wygenerować stronę z danego pliku html, tworząc zmienne możemy je przekazać na stronę i następnie je tam wywołać
        "home.html",
        title = "SimpleData"    #taka zmienna którą możemy wyświetlić na stronie
    )

@app.route('/login',methods=['GET', 'POST'])    #oprócz ścieżki dodajemmy tu metody jakie mogą być obsługiwane na stronie, w tym momencie robimy to aby ta strona mogła onsługiwać formularze
def login():
    form = LoginForm()  #do zmiennej form przypisujemy model formularza który będzie działał na tej stronie
    if form.validate_on_submit():   
        if form.email.data == 'admin@sd.com' and form.haslo.data == 'haslo':    #dal potrzeby sprawdzenia walidacji danych ustawione jest sztywne email i hasło po któym będzie się można zalogować
            flash('Udało się zalogować', 'success') #wiadomość która ma się pokazać po porawnym wpisaniu danych
            return redirect(url_for('home'))
        else:
            flash('Logowanie nie udane. Sprawdź poprawność danych a wrazie dalszych problemów skontaktuj się z administratorem', 'danger')  #wiadomość jeśli dane będą nie poprawne
    return render_template(
        "login.html",
        title = "Logowanie",
        form=form #rendereujemy stronę i przekzaujemy formularz
        )
@app.route('/rejestruj', methods=['GET', 'POST'])
def rejestr():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.Nazwa.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('rejestr.html', 
        title='Rejestracja',
        form=form
        )
