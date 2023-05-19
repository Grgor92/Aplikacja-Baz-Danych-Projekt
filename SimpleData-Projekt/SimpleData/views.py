# -*- coding: utf-8 -*-
from multiprocessing.connection import Connection
from asyncio.windows_events import NULL
from flask import render_template, jsonify, redirect, url_for, flash, session, request, Flask
from SimpleData import app, db, bcrypt, LoginManager
from datetime import datetime
from .forms import RegistrationForm, LoginForm, przeszukiwanie_d, dok_historyczne, kontrahenci_F, uzytkownicy, magazyn_towar, Users_zmiana, moje_ustawienia, DodajDokumentForm  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db, bcrypt
from .tabele import Uzytkownicy, Kontrahenci, Dokumenty
from sqlalchemy import inspect, text
from flask_login import login_user, logout_user, login_required, current_user, fresh_login_required

from flask_bcrypt import Bcrypt


#wewnątrz aplikacji 
#sprawdzenie czy baza danych istnieje
#with app.app_context():
##sprawdzenie czy baza danych istnieje
#    inspector = inspect(db.engine)
#    db.drop_all()
#    if not inspector.has_table('Uzytkownicy'):
#        db.create_all()
#    new_product = Uzytkownicy( imie='admin', email='sd@admin.com', haslo=bcrypt.generate_password_hash('haslo').decode('utf-8'), typ='Kierownik')
#    db.session.add(new_product)
#    db.session.commit()


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

    if form.validate_on_submit():   
            user = Uzytkownicy.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.haslo, form.haslo.data):
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
#@fresh_login_required
def rejestr():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.haslo.data).decode('utf-8')
        modyfikacja = Uzytkownicy(imie=form.Nazwa.data, email=form.email.data, haslo=hashed_password, typ=form.typ_uzytkownika.data) #przypisanie do zmiennej tabele z jej krotkami. Pobieramy dane do zmiany z formularza
        db.session.add(modyfikacja) #dodanie zmiennej modyfikacja do bazy
        db.session.commit() #wysłanie do bazy oraz zapisanie zmiany w niej
        flash(f'Konto stworzone! Zaloguj się.', 'success')
        return redirect(url_for('login'))
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

@app.route('/dokumenty', methods=['GET', 'POST'])
#@login_required
def dokumenty():
    form = dok_historyczne()
    form2 = DodajDokumentForm()
    query = text("SELECT * FROM Dokumenty WHERE numer_dokumentu = '' ;")
    result = db.session.execute(query)
    query3 = text("INSERT INTO Kontrahenci (NIP, nazwa_firmy, miasto, telefon, ulica, numer) SELECT '1234567890', 'Galicjanka', 'Galicja', 512512512, 'Galicyjska', '54A' FROM dual WHERE NOT EXISTS (SELECT * FROM Kontrahenci WHERE NIP = '1234567890');")
    db.session.execute(query3)
    query2 = text("INSERT INTO Dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_wykonania, data_waznosci_towaru, status) SELECT '12345', '2022-05-11', :user_id, 1234567890, 'PZ', '2022-05-11', '2022-06-11', 'Aktywna' FROM dual WHERE NOT EXISTS (SELECT * FROM Dokumenty WHERE numer_dokumentu = '12345');")
    db.session.execute(query2, {'user_id': current_user.id})
    db.session.commit()

    if form.validate_on_submit():
            query = 'SELECT d.*, k.nazwa_firmy FROM Dokumenty d JOIN Kontrahenci k ON d.NIP_kontrahenta = k.NIP WHERE d.status = "Aktywna"'
            params = {}
            if form.numer_dok.data:
                query += 'AND Dokumenty.numer_dokumentu = :numer_dokumentu '
                params['numer_dokumentu'] = form.numer_dok.data
            if form.data_wys.data:
                query += 'AND Dokumenty.data_wystawienia = :data_wystawienia '
                params['data_wystawienia'] = form.data_wys.data
            if form.id_klienta.data:
                query += 'AND Dokumenty.id_uzytkownika = :id_uzytkownika '
                params['id_uzytkownika'] = form.id_klienta.data
            if form.nip.data:
                query += 'AND Dokumenty.NIP_kontrahenta = :nip '
                params['nip'] = form.nip.data
            if form.rodzaj.data:
                query += 'AND Dokumenty.typ_dokumentu = :typ_dokumentu '
                params['typ_dokumentu'] = form.rodzaj.data
            if form.data_wyk.data:
                query += 'AND Dokumenty.data_wykonania = :data_wykonania '
                params['data_wykonania'] = form.data_wyk.data
            query = text(query)
            result = db.session.execute(query, params)
            db.session.commit()
    return render_template(
        "dokumenty.html",
        title = "SimpleData",
        #user = current_user.imie,
        form=form,
        form2=form2,
        values = result,
    )
    
@app.route('/dodaj_dokument_<dokument_type>', methods=['GET', 'POST'])
def dodaj_dokument(dokument_type):
    
    if dokument_type == 'PZ':
        form = DodajDokumentForm(rodzaj2='PZ')
    elif dokument_type == 'WZ':
        form = DodajDokumentForm(rodzaj2='WZ')
    query = text("SELECT * FROM Dokumenty WHERE status = 'Edycja' ;")
    result = db.session.execute(query)
    if request.method == 'POST' and form.validate_on_submit():
        rodzaj = dokument_type
        numer = request.form['numer_dok2']
        wys = request.form['data_wys2']
        nip = request.form['nip2']
        kontrahent = request.form['kontrahent2']
        data_wyk = request.form['data_wyk2']
        data_waz = request.form['data_waz2']
        status = 'Edycja'
        #dokument = Dokumenty(
        #    numer_dokumentu=numer,
        #    data_wystawienia=wys,
        #    id_uzytkownika=current_user.id,  
        #    NIP_kontrahenta=nip,
        #    typ_dokumentu=rodzaj,
        #    data_wykonania=data_wyk,
        #    data_waznosci_towaru=data_waz
        #)
        query = text('INSERT INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_wykonania, data_waznosci_towaru, status) VALUES (:numer, :wys, :id_uzytkownika, :nip, :rodzaj, :data_wyk, :data_waz, :status)')
        params = {
            'numer': numer,
            'wys': wys,
            'id_uzytkownika': current_user.id,
            'nip': nip,
            'rodzaj': rodzaj,
            'data_wyk': data_wyk,
            'data_waz': data_waz,
            'status': status
        }
    
        db.session.execute(query, params)
        #db.session.add(dokument)
        db.session.commit()

        flash(f'Dokument został dodany')
    form=DodajDokumentForm()   
    return render_template(
        "dod_dok.html",
        title="SimpleData",
        #user=current_user.imie,
        form2=form,
        typ=dokument_type,
        values=result
    )

        #query = text('SELECT Dokumenty.*, Kontrahenci.nazwa_firmy FROM Dokumenty JOIN Kontrahenci ON Dokumenty.NIP_kontrahenta = Kontrahenci.NIP WHERE Dokumenty.NIP_kontrahenta = :nip')
        #values = db.session.execute(query, {'nip': 1234567890})
        #flash(f'Zaktualizowano aktualnie zalogowanego użytkownika. Proszę zalogować się ponownie', 'success')
    #if form.validate_on_submit():
    #    query2 = text("INSERT INTO Dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_wykonania, data_waznosci_towaru) VALUES ('12345', '2022-05-11', 1, 1234567890, 'PZ', '2022-05-11', '2022-06-11');")
    #    db.session.execute(query2)
    #    db.session.commit()
    #    query = text('SELECT Dokumenty.*, Kontrahenci.nazwa_firmy FROM Dokumenty JOIN Kontrahenci ON Dokumenty.NIP_kontrahenta = Kontrahenci.NIP WHERE Dokumenty.NIP_kontrahenta = :nip')
    #    values = db.session.execute(query, {'nip': 1234567890})
    #    flash(f'Zaktualizowano aktualnie zalogowanego użytkownika. Proszę zalogować się ponownie', 'success')

    #return render_template(
    #    "dokumenty.html",
    #    title = "SimpleData",
    #    #user = current_user.imie,
    #    form=form,
    #    values = result
    #)



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

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    user_id = request.form['id']
    user = Uzytkownicy.query.filter_by(id=user_id).first()

    if user.imie != request.form['imie']:
        user.imie = request.form['imie']

    if user.haslo != request.form['haslo']:
        hashed_password = bcrypt.generate_password_hash(request.form['haslo']).decode('utf-8')
        user.haslo = hashed_password

    if user.email != request.form['email']:
        user.email = request.form['email']

    if user.typ != request.form['uprawnienia']:
        user.typ = request.form['uprawnienia']

    if db.session.dirty:
        db.session.commit()
        if current_user.id == int(user_id):
            flash(f'Zaktualizowano aktualnie zalogowanego użytkownika. Proszę zalogować się ponownie', 'success')
        return redirect(url_for('logout'))
    else:
        flash('Nie zmieniono danych, nie zakutaliwano użytkownika')
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

@app.route('/kontrahenci', methods=['GET', 'POST'])
@login_required
def kontrahenci_t():
    form = kontrahenci_F()
    kontrahenci = Kontrahenci.query.all()
    return render_template(
        "kontrahenci.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form,
        kontrahenci=kontrahenci
    )

#@app.route('/kontrahenci')
#def kontrahenci():
#    # Pobranie danych z bazy
    

#    # Renderowanie szablonu HTML z danymi z bazy
#    return render_template('kontrahenci.html', kontrahenci=kontrahenci)



@app.route('/dodaj_rekord', methods=['POST'])
def dodaj_rekord():
    nip = request.form.get('nip')
    nazwa_firmy = request.form.get('nazwa_firmy')
    miasto = request.form.get('miasto')
    nr_telefonu = request.form.get('nr_telefonu')
    ulica = request.form.get('ulica')
    numer = request.form.get('numer')

    kontrahent = Kontrahenci(NIP=nip, nazwa_firmy=nazwa_firmy, miasto=miasto, telefon=nr_telefonu, ulica=ulica, numer=numer)
    db.session.add(kontrahent)
    db.session.commit()

    return redirect(url_for('kontrahenci_t'))