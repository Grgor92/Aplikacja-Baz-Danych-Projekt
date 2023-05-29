from flask import Blueprint, render_template, redirect, url_for, flash, session, request, Flask
from SimpleData import app, db
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
        kontrahent = form.Firma.data
        query = "INSERT INTO towary (NIP, typ, rodzaj, nazwa) VALUES (:nip, :typ, :rodzaj, :nazwa)"
        params = {'nip': kontrahent.NIP, 'typ': form.Typ.data, 'rodzaj': form.Rodzaj.data, 'nazwa': form.Nazwa.data}
        #if form.NIP.data:
        #    query += 'AND NIP = :NIP '
        #    params['NIP'] = form.NIP.data
        #if form.Typ.data:
        #    query += 'AND Typ = :Typ '
        #    params['Typ'] = form.Typ.data
        #if form.Rodzaj.data:
        #    query += 'AND Rodzaj = :Rodzaj '
        #    params['Rodzaj'] = form.Rodzaj.data
        #if form.Nazwa.data:
        #    query += 'AND Nazwa = :Nazwa '
        #    params['Nazwa'] = form.Nazwa.data
        query = text(query)
        result = db.session.execute(query, params)
        db.session.commit()
        return redirect(url_for('tow.wypis_towary'))
    # dodaj formularz form = kontrahenci()
    #wyrenderuj strone ze wzoru
    return render_template(
        "towary.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        form=form
    )

@tow.route('/edytuj_towar/<towar_id>', methods=['GET', 'POST'])
@login_required
def edytuj_towar(towar_id):
    form = FiltrujDaneTowaryDostawcy()
    towar_id=towar_id
    #query = 'Select * from Towary WHERE id_towaru= :ide '
    #result = db.session.execute(text(query), {"ide": towar_id})
    rekord = Towary.query.filter_by(id_towaru=towar_id).first()
     # Przypisz wartości pól formularza na podstawie danych z bazy danych


    if form.validate_on_submit():
        if form.NIP.data != rekord.NIP:
            rekord.NIP = form.NIP.data

        if form.Typ.data != rekord.typ:
            rekord.typ = form.Typ.data

        if form.Rodzaj.data != rekord.rodzaj:
            rekord.rodzaj = form.Rodzaj.data

        if form.Nazwa.data != rekord.nazwa:
            rekord.nazwa = form.Nazwa.data

        if db.session.dirty:
            db.session.commit()
            flash('Dane zostały zaktualizowane.', 'success')
            return redirect(url_for('tow.wypis_towary'))
        else:
            flash('Nie zmieniono danych, nie zaktualizowano rekordu.', 'warning')

    form.NIP.data = rekord.NIP
    form.Typ.data = rekord.typ
    form.Rodzaj.data = rekord.rodzaj
    form.Nazwa.data = rekord.nazwa
    return render_template( 
        "edytuj_towar.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        #
        form=form,
    )

#usun towar z wiersza wybranego

@tow.route('/usun_towar/<towar_id>', methods=['GET', 'POST'])
@login_required
def usun_towar(towar_id):
    form = FiltrujDaneTowaryDostawcy()
    
    try:
        Session = sessionmaker(bind=db.engine)
        # Usuwanie rekordu po towar_id
        rekord = Towary.query.filter_by(id_towaru=towar_id).first()
        #rekord = session.query(Towary).filter_by(id_towaru=towar_id).first()

        if rekord:
            db.session.delete(rekord)
            db.session.commit()
            flash('Rekord został usunięty.', 'success')
            return redirect(url_for('tow.wypis_towary'))
        else:
            flash('Nie znaleziono rekordu o podanym towar_id.', 'warning')
    
    except SQLAlchemyError as e:
        flash('Wystąpił błąd podczas usuwania rekordu.', 'error')
        session.rollback()
    
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
    query = 'Select * from towary WHERE 1=1 '
    result = db.session.execute(text(query))
    if form.validate_on_submit():
        
        params = {}
        if form.NIP.data:
            query += 'AND NIP = :NIP '
            params['NIP'] = form.NIP.data
        if form.Typ.data:
            query += 'AND Typ = :Typ '
            params['Typ'] = form.Typ.data
        if form.Rodzaj.data:
            query += 'AND Rodzaj = :Rodzaj '
            params['Rodzaj'] = form.Rodzaj.data
        if form.Nazwa.data:
            query += 'AND Nazwa = :Nazwa '
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
        #
        form=form,
        values = result,
    )