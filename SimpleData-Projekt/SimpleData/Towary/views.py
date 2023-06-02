from flask import Blueprint, render_template, redirect, url_for, flash, session, request, Flask
from SimpleData import app, db, roles_required
from SimpleData.Towary.forms import DodajDokumentForm, FiltrujDaneTowaryDostawcy, DodajDaneTowaryDostawcy  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import uzytkownicy, Kontrahenci, dokumenty, Towary
from sqlalchemy import inspect, text, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user, fresh_login_required

tow = Blueprint('tow', __name__)

@tow.route('/towary', methods=['GET', 'POST'])
@login_required
def towary():
    form=DodajDaneTowaryDostawcy()
    if form.validate_on_submit():
        if current_user.typ == 'Administrator' or current_user.typ == 'Kierownik':
            kontrahent = form.Firma.data
            query = "INSERT INTO towary (NIP, typ, rodzaj, nazwa, stan) VALUES (:nip, :typ, :rodzaj, :nazwa, 'Aktywna')"
            params = {'nip': kontrahent.NIP, 'typ': form.Typ.data, 'rodzaj': form.Rodzaj.data, 'nazwa': form.Nazwa.data}
            query = text(query)
            result = db.session.execute(query, params)
            db.session.commit()
            return redirect(url_for('tow.wypis_towary'))
        #wyrenderuj strone ze wzoru
    return render_template(
        "towary.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        form=form
    )

@tow.route('/edytuj_towar/<towar_id>', methods=['GET', 'POST'])
@roles_required('Administrator')
def edytuj_towar(towar_id):
    form = FiltrujDaneTowaryDostawcy()
    rekord = Towary.query.filter_by(id_towaru=towar_id).first()
    form.NIP.data=rekord.NIP
    form.Typ.data=rekord.typ
    form.Rodzaj.data=rekord.rodzaj
    form.Nazwa.data=rekord.nazwa


    if form.validate_on_submit():
        if rekord:
            # Stwórz nowy rekord z aktualizowanymi wartościami i stanem "Aktywny"
            nowy_rekord = Towary(
                NIP=form.NIP.data,
                typ=form.Typ.data,
                rodzaj=form.Rodzaj.data,
                nazwa=form.Nazwa.data,
                stan="Aktywny"
            )
            db.session.add(nowy_rekord)
            db.session.commit()

            # Zmień stan istniejącego rekordu na "Nieaktualny"
            rekord.stan = "Nieaktualny"
            db.session.commit()

            flash('Dane zostały zaktualizowane.', 'success')
            return redirect(url_for('tow.wypis_towary'))
        else:
            flash('Rekord o podanym ID nie istnieje.', 'danger')
            return redirect(url_for('tow.wypis_towary'))
    return render_template( 
        "edytuj_towar.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        #
        form=form,
    )

#usun towar z wiersza wybranego

@tow.route('/usun_towar/<towar_id>', methods=['GET', 'POST'])
@roles_required('Administrator')
@login_required
def usun_towar(towar_id):
    form = FiltrujDaneTowaryDostawcy()

    try:
        # Znajdź rekord towaru na podstawie towar_id
        rekord = Towary.query.filter_by(id_towaru=towar_id).first()

        if rekord:
            # Zmień stan rekordu na "Nieaktualny"
            rekord.stan = "Nieaktualny"
            db.session.commit()
            flash('Stan rekordu został zmieniony na "Nieaktualny".', 'success')
            return redirect(url_for('tow.wypis_towary'))
        else:
            flash('Nie znaleziono rekordu o podanym towar_id.', 'warning')

    except SQLAlchemyError as e:
        flash('Wystąpił błąd podczas zmiany stanu rekordu.', 'error')
        db.session.rollback()
    
    return render_template(
        "usun_towar.html",
        title="SimpleData",
        user=current_user.imie,
        form=form,
    )


@tow.route('/wypis-towary', methods=['GET', 'POST'])
@login_required
def wypis_towary():
    form = FiltrujDaneTowaryDostawcy()
    query = 'Select * from towary WHERE stan="Aktywna" '
    result = db.session.execute(text(query))
    if form.validate_on_submit():
        
        params = {}
        if form.NIP.data:
            query += 'AND NIP LIKE :NIP '
            params['NIP'] = form.NIP.data
        if form.Typ.data:
            query += 'AND Typ LIKE :Typ '
            params['Typ'] = form.Typ.data
        if form.Rodzaj.data:
            query += 'AND Rodzaj LIKE :Rodzaj '
            params['Rodzaj'] = form.Rodzaj.data
        if form.Nazwa.data:
            query += 'AND Nazwa LIKE :Nazwa '
            params['Nazwa'] = form.Nazwa.data
        query = text(query)
        result = db.session.execute(query, params)
        db.session.commit()
    # dodaj formularz form = kontrahenci()
    #wyrenderuj strone ze wzoru
    return render_template( 
        "wypis_towary.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        form=form,
        values = result,
    )