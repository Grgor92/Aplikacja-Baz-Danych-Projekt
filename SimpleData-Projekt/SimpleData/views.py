﻿# -*- coding: utf-8 -*-
from flask import render_template, jsonify, redirect, url_for, flash, session
from SimpleData import app
from datetime import datetime
from .forms import RegistrationForm, LoginForm, przeszukiwanie # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db
from .tabele import Users
from sqlalchemy import inspect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, fresh_login_required

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.sesion = True

login_manager.unauthorized

@login_manager.unauthorized_handler
def unauthorized():
    flash('Musisz się zalogować, aby uzyskać dostęp do tej strony!', 'danger')
    return redirect(url_for('home'))

# deklaracja funkcji do pobierania użytkownika po jego id
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

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
    user = current_user.nazwa if current_user.is_authenticated else None
    return render_template( #używamy render_teamplate aby wygenerować stronę z danego pliku html, tworząc zmienne możemy je przekazać na stronę i następnie je tam wywołać
        "home.html",
        title = "SimpleData",    #taka zmienna którą możemy wyświetlić na stronie
        user=user
    )
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/login',methods=['GET', 'POST'])    #oprócz ścieżki dodajemmy tu metody jakie mogą być obsługiwane na stronie, w tym momencie robimy to aby ta strona mogła onsługiwać formularze
def login():
    form = LoginForm()  #do zmiennej form przypisujemy model formularza który będzie działał na tej stronie
    if form.validate_on_submit():   
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.haslo == form.haslo.data:
            login_user(user)
            flash('Udało się zalogować', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logowanie nie udane. Sprawdź poprawność danych a wrazie dalszych problemów skontaktuj się z administratorem', 'danger')  #wiadomość jeśli dane będą nie poprawne
    return render_template(
        "login.html",
        title = "Logowanie",
        user = current_user.nazwa if current_user.is_authenticated else None,
        form=form #rendereujemy stronę i przekzaujemy formularz
        )
@app.route('/rejestruj', methods=['GET', 'POST'])
@login_required
def rejestr():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.Nazwa.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('rejestr.html', 
        title='Rejestracja',
        user = current_user.nazwa if current_user.is_authenticated else None,
        form=form
        )
@app.route('/podsumowanie', methods=['GET', 'POST'])
@fresh_login_required
def podsumowanie():
    form = przeszukiwanie()
    return render_template(
        "podsumowanie.html",
        title = "SimpleData",
        user = current_user.nazwa,
        form=form
    )
