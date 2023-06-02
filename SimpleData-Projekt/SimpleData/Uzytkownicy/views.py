from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request
from SimpleData import db, bcrypt, roles_required
from SimpleData.Uzytkownicy.forms import RegistrationForm, LoginForm, Uzytkownicy, Users_zmiana, moje_ustawienia  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import uzytkownicy
from sqlalchemy import text
from flask_login import login_user, login_required, current_user
from flask_bcrypt import generate_password_hash, check_password_hash

users = Blueprint('users', __name__)

@users.route('/login',methods=['GET', 'POST'])    #oprócz ścieżki dodajemmy tu metody jakie mogą być obsługiwane na stronie, w tym momencie robimy to aby ta strona mogła onsługiwać formularze
def login():
    form = LoginForm()  #do zmiennej form przypisujemy model formularza który będzie działał na tej stronie
    if current_user.is_authenticated:
        return redirect(url_for('ogolne.home'))

    if form.validate_on_submit():   
            user = uzytkownicy.query.filter_by(email=form.email.data, stan="Aktywny").first()
            if user and bcrypt.check_password_hash(user.haslo, form.haslo.data):
                login_user(user)
                flash('Udało się zalogować', 'success')
                return redirect(url_for('ogolne.home'))
            else:
                flash('Logowanie nie udane. Sprawdź poprawność danych a wrazie dalszych problemów skontaktuj się z administratorem', 'danger')  #wiadomość jeśli dane będą nie poprawne
    return render_template(
        "login.html",
        title = "Logowanie",
        user = current_user.imie if current_user.is_authenticated else None,
        form=form #rendereujemy stronę i przekzaujemy formularz
        )
@users.route('/rejestruj', methods=['GET', 'POST'])
@roles_required('Administrator')
def rejestr():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.haslo.data).decode('utf-8')
        modyfikacja = uzytkownicy(imie=form.Nazwa.data, email=form.email.data, haslo=hashed_password, typ=form.typ_uzytkownika.data, stan="Aktywny") #przypisanie do zmiennej tabele z jej krotkami. Pobieramy dane do zmiany z formularza
        db.session.add(modyfikacja) #dodanie zmiennej modyfikacja do bazy
        db.session.commit() #wysłanie do bazy oraz zapisanie zmiany w niej
        flash(f'Konto stworzone! Zaloguj się.', 'success')
        return redirect(url_for('users.login'))
    return render_template('rejestr.html', 
        title='Rejestracja',
        user = current_user.imie if current_user.is_authenticated else None,
        form=form
        )

@users.route('/uzytkownicy', methods=['GET', 'POST'])
@login_required
def uzytkownicy_t():
    form = Uzytkownicy()
    form2 = Users_zmiana()
    values = uzytkownicy.query.filter_by(typ='').all()
    if form.validate_on_submit():
        values=uzytkownicy.query.all()
        query = 'SELECT * FROM uzytkownicy WHERE stan="Aktywny" '
        params = {}
        if form.imie.data:
            query += 'AND imie LIKE :imie '
            params['imie'] = form.imie.data
        if form.email.data:
            query += 'AND email LIKE :email '
            params['email'] = form.email.data
        if form.typ.data:
            query += 'AND typ LIKE :typ '
            params['typ'] = form.typ.data
        query = text(query)
        values = db.session.execute(query, params)
        db.session.commit()    
    return render_template(
            "uzytkownicy.html",
            title = "SimpleData",
            user = current_user.imie,
            form=form,
            form2=form2,
            values=values
        )

@users.route('/edit_user', methods=['GET', 'POST'])
@roles_required('Administrator')
def edit_user():
    user_id = request.form['id']
    user = uzytkownicy.query.filter_by(id=user_id).first()

    if user.imie != request.form['imie']:
        user.imie = request.form['imie']

    if user.haslo != request.form['haslo'] and request.form['haslo']:
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
        return redirect(url_for('ogolne.logout'))
    else:
        flash('Nie zmieniono danych, nie zakutaliwano użytkownika')
        return redirect(url_for('users.uzytkownicy_t'))


@users.route('/uzytkownicy', methods=['GET', 'POST'])
@login_required
def ustawienia_kont():
    form = moje_ustawienia()

    if form.validate_on_submit():
        current_user.imie = form.username.data
        current_user.email = form.email.data

        # Sprawdzenie poprawności hasła przed zapisaniem zmian
        if form.password.data:
            if check_password_hash(current_user.haslo, form.password.data):
                # Hasło się zgadza, można zaktualizować
                new_password_hash = generate_password_hash(form.new_password.data)
                current_user.haslo = new_password_hash
            else:
                flash('Podano nieprawidłowe hasło.', 'error')
                return redirect(url_for('users.ustawienia_kont'))

        db.session.commit()
        flash('Twoje ustawienia zostały zaktualizowane.', 'success')
        return redirect(url_for('users.ustawienia_kont'))

    form.username.data = current_user.imie
    form.email.data = current_user.email

    return render_template('ustawienia_kont.html', form=form, imie=current_user.imie, email=current_user.email)

@users.route('/uzytkownicy/<int:ide>', methods=['DELETE'])
@roles_required('Administrator')
def delete_user(ide):
    if ide == 1:
        message = {'message': 'Tego użytkownika nie można usunąć.'}
        status_code = 200
    else:
        user = uzytkownicy.query.filter_by(id=ide).first()
        if user:
            user.stan = 'Usuniete'  # Zmiana wartości w kolumnie 'stan' na 'Usuniete'
            db.session.commit()
            message = {'message': 'Użytkownik został usunięty.'}
            status_code = 200
        else:
            message = {'message': 'Użytkownik o podanym id nie został znaleziony.'}
            status_code = 404
    return jsonify(message), status_code
