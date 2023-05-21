from flask import Blueprint, render_template, redirect, url_for, flash, session, request, Flask
from SimpleData import app, db 
from SimpleData.Towary.forms import DodajDokumentForm, FiltrujDaneTowaryDostawcy, DodajDaneTowaryDostawcy  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty, Towary
from sqlalchemy import inspect, text
from flask_login import login_required, current_user, fresh_login_required

tow = Blueprint('tow', __name__)

@tow.route('/towary', methods=['GET', 'POST'])
@login_required
def towary():
    form=DodajDaneTowaryDostawcy()
    if form.validate_on_submit():
        kontrahent = form.Firma.data
        query = "INSERT INTO Towary (NIP, typ, rodzaj, nazwa) VALUES (:nip, :typ, :rodzaj, :nazwa)"
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

@tow.route('/wypis-towary', methods=['GET', 'POST'])
@login_required
def wypis_towary():
    form = FiltrujDaneTowaryDostawcy()
    query = 'Select * from Towary WHERE 1=1 '
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