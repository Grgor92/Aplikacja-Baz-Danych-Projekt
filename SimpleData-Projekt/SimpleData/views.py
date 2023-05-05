# -*- coding: utf-8 -*-
from flask import render_template, jsonify, redirect, url_for, flash, session, request
from SimpleData import app
from datetime import datetime
from .forms import RegistrationForm, LoginForm, przeszukiwanie_d, dok_historyczne, kontrahenci, uzytkownicy, magazyn_towar, Users_zmiana # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db
from .tabele import Users
from sqlalchemy import inspect
from flask_login import login_user, logout_user, login_required, current_user, fresh_login_required


#wewnątrz aplikacji 
with app.app_context():
#sprawdzenie czy tabela istnieje
    inspector = inspect(db.engine)
    #db.drop_all()
    if not inspector.has_table('Users'):
        db.create_all()
    new_product = Users(nazwa='admin2', email='sd@admin.com', haslo='haslo', uprawnienia='Kierownik')
    db.session.add(new_product)
    db.session.commit()

@app.route('/api/time') # ustawiamy ścieżkę po jakiej będzie można się dostać do danej wartości/strony po wpisaniu w przeglądarkę
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
@fresh_login_required
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
@app.route('/przeszukiwanie', methods=['GET', 'POST'])
@login_required
def przeszukiwanie():
    form = przeszukiwanie_d()
    return render_template(
        "przeszukiwanie.html",
        title = "SimpleData",
        user = current_user.nazwa,
        form=form
    )
@app.route('/dokumenty_historyczne', methods=['GET', 'POST'])
@login_required
def dokumenty_hist():
    form = dok_historyczne()
    return render_template(
        "dokumenty_historyczne.html",
        title = "SimpleData",
        user = current_user.nazwa,
        form=form
    )

@app.route('/kontrahenci', methods=['GET', 'POST'])
@login_required
def kontrahenci_t():
    form = kontrahenci()
    return render_template(
        "kontrahenci.html",
        title = "SimpleData",
        user = current_user.nazwa,
        form=form
    )
@app.route('/uzytkownicy', methods=['GET', 'POST'])
@login_required
def uzytkownicy_t():
    form = uzytkownicy()
    form2 = Users_zmiana()
    values = Users.query.filter_by(uprawnienia='')
    if form.validate_on_submit():
        values=Users.query.all()
    #if form2.validate_on_submit():
    #    user = Users.query.get(form2.id.data)
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
            user = current_user.nazwa,
            form=form,
            form2=form2,
            values=values
        )

@app.route('/edit_user', methods=['POST'])
def edit_user():
    user_id = request.form['id']
    user = Users.query.filter_by(id=user_id).first()
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
        user = current_user.nazwa,
        form=form
    )

def powrot():
    return redirect(request.referrer or url_for('home'))



#@app.route('/edit', methods=['POST'])
#def edit_user():
#    # kod do aktualizacji rekordu w bazie danych
#    # pobierz dane z formularza
#    id = request.form.get('id')
#    nazwa = request.form.get('nazwa')
#    email = request.form.get('email')
#    uprawnienia = request.form.get('uprawnienia')
#    # zaktualizuj rekord w bazie danych
#    # wyślij komunikat o sukcesie lub błędzie
    
#    return redirect(url_for('uzytkownicy_t'))