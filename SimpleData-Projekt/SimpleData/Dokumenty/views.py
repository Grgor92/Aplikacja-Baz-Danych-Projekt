from flask import Blueprint, render_template, redirect, url_for, flash, request
from SimpleData import app, db
from SimpleData.Dokumenty.forms import  dok_historyczne, DodajDokumentForm  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty
from sqlalchemy import text
from flask_login import login_required, current_user, fresh_login_required

dok = Blueprint('dok', __name__)


@dok.route('/dokumenty', methods=['GET', 'POST'])
#@login_required
def dokumenty():
    form = dok_historyczne()
    form2 = DodajDokumentForm()
    query = text("SELECT * FROM Dokumenty WHERE numer_dokumentu = '' ;")
    result = db.session.execute(query)
    query3 = text("INSERT INTO Kontrahenci (NIP, nazwa_firmy, miasto, telefon, ulica, numer, rodzaj) SELECT '1234567890', 'Galicjanka', 'Galicja', 512512512, 'Galicyjska', '54A', 'Odbiorca' FROM dual WHERE NOT EXISTS (SELECT * FROM Kontrahenci WHERE NIP = '1234567890');")
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
    
@dok.route('/dodaj_dokument_<dokument_type>', methods=['GET', 'POST'])
def dodaj_dokument(dokument_type):
    
    if dokument_type == 'PZ':
        form = DodajDokumentForm(rodzaj2='PZ')
    elif dokument_type == 'WZ':
        form = DodajDokumentForm(rodzaj2='WZ')
    query = text("SELECT * FROM Dokumenty WHERE status = 'Edycja' ;")
    result = db.session.execute(query)
    if form.validate_on_submit():
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
#    # -*- coding: utf-8 -*-
#from multiprocessing.connection import Connection
#from asyncio.windows_events import NULL
#from flask import render_template, jsonify, redirect, url_for, flash, session, request, Flask
#from SimpleData import app, db, bcrypt, LoginManager
#from datetime import datetime
#from .forms import RegistrationForm, LoginForm, przeszukiwanie_d, dok_historyczne, kontrahenci_F, uzytkownicy, magazyn_towar, Users_zmiana, moje_ustawienia, DodajDokumentForm  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
#from SimpleData import db, bcrypt
#from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty
#from sqlalchemy import inspect, text
#from flask_login import login_user, logout_user, login_required, current_user, fresh_login_required
#from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash