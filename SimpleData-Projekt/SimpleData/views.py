# -*- coding: utf-8 -*-
from multiprocessing.connection import Connection
import sqlite3
from asyncio.windows_events import NULL
from flask import render_template, jsonify, redirect, url_for, flash, session, request, Flask
from SimpleData import app
from datetime import datetime
from .forms import RegistrationForm, LoginForm, przeszukiwanie_d, dok_historyczne, kontrahenci, uzytkownicy, magazyn_towar, Users_zmiana, moje_ustawienia, WyszukajKontrahenta  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db
from .tabele import Uzytkownicy, Kontrahenci
from sqlalchemy import inspect
from flask_login import login_user, logout_user, login_required, current_user, fresh_login_required

#wewnątrz aplikacji 
#with app.app_context():
#sprawdzenie czy baza danych istnieje
    #inspector = inspect(db.engine)
    #db.drop_all()
    #if not inspector.has_table('Uzytkownicy'):
    #    db.create_all()
    #new_product = Uzytkownicy( imie='admin', email='sd@admin.com', haslo='haslo', typ='Kierownik')
    #db.session.add(new_product)
    #db.session.commit()

@app.route('/api/time') # ustawiamy ścieżkę po jakiej będzie można się dostać do danej wartości/strony po wpisaniu w przeglądarkę
def current_time():
    now = datetime.now()  #pobieramy obecny czas z systemu
    formatted_now = now.strftime("%A, %d %B, %Y %H:%M") #ustalamy w jakim formacie będzie wyświetlany czas
    return jsonify({'time': formatted_now})

@app.route('/')
@app.route('/home') #Aby dana strona była dostępna pod dwoma ścieżkami wystarczy dodać pod sobą dwie linie kodu @app.route
def home():
    user = current_user.imie if current_user.is_authenticated else None
    return render_template( #używamy render_teamplate aby wygenerować stronę z danego pliku html, tworząc zmienne możemy je przekazać na stronę i następnie je tam wywołać
        "home.html",
        title = "SimpleData",    #taka zmienna którą możemy wyświetlić na stronie
        user=user
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/login',methods=['GET', 'POST'])    #oprócz ścieżki dodajemmy tu metody jakie mogą być obsługiwane na stronie, w tym momencie robimy to aby ta strona mogła onsługiwać formularze
def login():
    form = LoginForm()  #do zmiennej form przypisujemy model formularza który będzie działał na tej stronie
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        if form.validate_on_submit():   
            user = Uzytkownicy.query.filter_by(email=form.email.data).first()
            if user and user.haslo == form.haslo.data:
                login_user(user)
                flash('Udało się zalogować', 'success')
                return redirect(url_for('home'))
            else:
                flash('Logowanie nie udane. Sprawdź poprawność danych a wrazie dalszych problemów skontaktuj się z administratorem', 'danger')  #wiadomość jeśli dane będą nie poprawne
    return render_template(
        "login.html",
        title = "Logowanie",
        user = current_user.imie if current_user.is_authenticated else None,
        form=form #rendereujemy stronę i przekzaujemy formularz
        )
@app.route('/rejestruj', methods=['GET', 'POST'])
@fresh_login_required
def rejestr():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.Nazwa.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('rejestr.html', 
        title='Rejestracja',
        user = current_user.imie if current_user.is_authenticated else None,
        form=form
        )
@app.route('/przeszukiwanie', methods=['GET', 'POST'])
@login_required
def przeszukiwanie():
    form = przeszukiwanie_d()
    return render_template(
        "przeszukiwanie.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form
    )
@app.route('/dokumenty_historyczne', methods=['GET', 'POST'])
@login_required
def dokumenty_hist():
    form = dok_historyczne()
    return render_template(
        "dokumenty_historyczne.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form
    )

@app.route('/kontrahenci', methods=['GET', 'POST'])
@login_required
def kontrahenci_t():
    form = kontrahenci()
    return render_template(
        "kontrahenci.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form
    )
@app.route('/uzytkownicy', methods=['GET', 'POST'])
@login_required
def uzytkownicy_t():
    form = uzytkownicy()
    form2 = Users_zmiana()
    values = Uzytkownicy.query.filter_by(typ='').all()
    if form.validate_on_submit():
        values=Uzytkownicy.query.all()
    #if form2.validate_on_submit():
    #    user = Uzytkownicy.query.get(form2.id.data)
    #    if user:
    #        user.imie = form2.imie.data
    #        user.email = form2.email.data
    #        user.uprawnienia = form2.uprawnienia.data
    #        db.session.commit()
    #        flash('Zaktualizowano użytkownika', 'success')
    #        return redirect(url_for('home'))
    #    else:
    #        return redirect(url_for('home'))
    
    return render_template(
            "uzytkownicy.html",
            title = "SimpleData",
            user = current_user.imie,
            form=form,
            form2=form2,
            values=values
        )


@app.route('/edit_user', methods=['POST'])
def edit_user():
    user_id = request.form['id']
    user = Uzytkownicy.query.filter_by(id=user_id).first()
    user.nazwa = request.form['imie']
    user.haslo = request.form['haslo']
    user.email = request.form['email']
    user.uprawnienia = request.form['uprawnienia']
    db.session.commit()
    flash('Zaktualizowano użytkownika', 'success')
    return redirect(url_for('uzytkownicy_t'))
    
@app.route('/magazyn_towar', methods=['GET', 'POST'])
@login_required
def magazyn_towar_t():
    form = magazyn_towar()
    return render_template(
        "magazyn_towar.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form
    )

@app.route('/ustawienia')
@login_required
def ustawieniakont():
    
    form = moje_ustawienia()
    if request.method == 'POST':
        nazwa = request.form['Nazwa']
        password = request.form['Hasło']
        password2 = request.form['Powtórz hasło']
        
        if not nazwa or not password or not password2:
            # błędy walidacji
            pass
        
        if password != password2:
            # błędy walidacji
            pass
        
        current_user.nazwa = username
        current_user.set_password(password)
        db.session.commit()
        
        # przekierowanie użytkownika na stronę główną ustwaień
        pass
    else:
        return render_template(
            'ustawienia_kont.html',
            form=form
        )

@app.route('/ustawienia')
@login_required
def ustawienia_kont():
    username = current_user.nazwa
    email = current_user.email
    return render_template('ustawienia_kont.html', nazwa=username, email=email)


@app.route('/query', methods=['POST'])
def dodaj_rekord():
    nip = request.form['nip']
    nazwa_firmy = request.form['nazwa_firmy']
    miasto = request.form['miasto']
    nr_telefonu = request.form['nr_telefonu']
    ulica = request.form['ulica']
    numer = request.form['numer']

    kontrahenci = Kontrahenci(NIP=nip, nazwa_firmy=nazwa_firmy, miasto=miasto, telefon=nr_telefonu, ulica=ulica, numer=numer)
    db.session.add(kontrahenci)
    db.session.commit()

    return redirect(url_for("kontrahenci_t"))

if __name__ == '__main__':
    app.run()


@app.route('/wyszukaj', methods=['POST'])
def wyszukaj_rekordy():
    form = WyszukajKontrahenta(request.form)
    if form.validate():
        nip = form.nip.data
        nazwa_firmy = form.nazwa_firmy.data
        # Wykonaj operacje wyszukiwania na podstawie NIP i nazwy firmy
        return render_template('kontrahenci.html', kontrahenci=wyniki_wyszukiwania)
    else:
        flash('Wprowadź poprawne wartości do formularza')
        return redirect(url_for('kontrahenci_t'))


from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/kontrahenci')
def kontrahenci():
    # Pobranie danych z bazy
    kontrahenci = Kontrahenci.query.all()

    # Renderowanie szablonu HTML z danymi z bazy
    return render_template('kontrahenci.html', kontrahenci=kontrahenci)

if __name__ == '__main__':
    app.run()
