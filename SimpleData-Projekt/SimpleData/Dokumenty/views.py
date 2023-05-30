from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request
from SimpleData import app, db
from SimpleData.Dokumenty.forms import  dok_historyczne, DodajDokumentForm, DodajTowarDokument  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import uzytkownicy, Kontrahenci, dokumenty, TowaryDokument
from sqlalchemy import text
from flask_login import login_required, current_user, fresh_login_required
from datetime import date

dok = Blueprint('dok', __name__)


@dok.route('/dokumenty', methods=['GET', 'POST'])
#@login_required
def dokumenty():
    form = dok_historyczne()
    query = text("SELECT * FROM dokumenty WHERE numer_dokumentu = '' ;")
    result = db.session.execute(query)
    query3 = text("INSERT IGNORE INTO kontrahenci (NIP, nazwa_firmy, miasto, telefon, ulica, numer, status) VALUES ('1234567890', 'Galicjanka', 'Galicja', 512512512, 'Galicyjska', '54A', 'Dostawca');")
    db.session.execute(query3)
    query2 = text("INSERT IGNORE INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_wykonania, data_waznosci_towaru, statusd) VALUES ('12345', '2022-05-11', :user_id, 1234567890, 'PZ', '2022-05-11', '2022-06-11', 'Aktywna');")
    db.session.execute(query2, {'user_id': current_user.id})
    db.session.commit()

    if form.validate_on_submit():
        query = 'SELECT d.*, k.nazwa_firmy, u.imie FROM dokumenty d JOIN kontrahenci k ON d.NIP_kontrahenta = k.NIP JOIN uzytkownicy u ON d.id_uzytkownika = u.id'
        filters = {
            'numer_dokumentu': 'd.numer_dokumentu = :numer_dokumentu',
            'data_wystawienia': 'd.data_wystawienia = :data_wystawienia',
            'id_uzytkownika': 'd.id_uzytkownika = :id_uzytkownika',
            'NIP_kontrahenta': 'd.NIP_kontrahenta = :NIP_kontrahenta',
            'typ_dokumentu': 'd.typ_dokumentu = :typ_dokumentu',
            'data_wykonania': 'd.data_wykonania = :data_wykonania',
            'statusd': 'd.statusd = :statusd'
        }

        conditions = []
        params = {}

        for field, condition in filters.items():
            if getattr(form, field).data:
                conditions.append(condition)
                params[field] = getattr(form, field).data

        if conditions:
            query += ' AND ' + ' AND '.join(conditions)

        result = db.session.execute(text(query), params)
        db.session.commit()
    return render_template(
        "dokumenty.html",
        title = "SimpleData",
        #user = current_user.imie,
        form=form,
        values = result,
    )
    
@dok.route('/dokumenty/dodaj_dokument_<dokument_type>', methods=['GET', 'POST'])
def dodaj_dokument(dokument_type):
    if dokument_type == 'PZ':
        form = DodajDokumentForm(rodzaj2='PZ')
    elif dokument_type == 'WZ':
        kontrahenci = Kontrahenci.query.filter_by(status='Odbiorca').all()  # Pobierz odpowiednich kontrahentów z bazy danych
        form = DodajDokumentForm(rodzaj2='WZ', kontrahent2=kontrahenci)

    query = text('SELECT d.*, k.nazwa_firmy FROM dokumenty d JOIN kontrahenci k ON d.NIP_kontrahenta = k.NIP WHERE d.statusd = "Edycja"')
    result = db.session.execute(query)
    if form.validate_on_submit() and request.method == 'POST':
        rodzaj = dokument_type
        numer = form.numer_dok2.data
        wys = form.data_wys2.data
        nip = form.nip2.data
        kontrahent = form.kontrahent2.data
        data_wyk = form.data_wyk2.data
        data_waz = form.data_waz2.data
        status = 'Edycja'
        #dokument = dokumenty(
        #    numer_dokumentu=numer,
        #    data_wystawienia=wys,
        #    id_uzytkownika=current_user.id,  
        #    NIP_kontrahenta=nip,
        #    typ_dokumentu=rodzaj,
        #    data_wykonania=data_wyk,
        #    data_waznosci_towaru=data_waz
        #)
        query = text('INSERT INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_wykonania, data_waznosci_towaru, statusd, imie_uzytkownika) VALUES (:numer, :wys, :id_uzytkownika, :nip, :rodzaj, :data_wyk, :data_waz, :status, :imie_uzy)')
        params = {
            'numer': numer,
            'wys': wys,
            'id_uzytkownika': current_user.id,
            'nip': nip,
            'rodzaj': rodzaj,
            'data_wyk': data_wyk,
            'data_waz': data_waz,
            'status': status,
            'imie_uzy': current_user.imie
        }

        db.session.execute(query, params)
        db.session.commit()
        flash('Dokument został dodany') 
        return redirect(url_for('dok.dodaj_dokument', dokument_type=form.rodzaj2.data))

    
        #db.session.execute(query, params)
        ##db.session.add(dokument)
        #db.session.commit()
        #flash(f'Dokument został dodany') 
        #return redirect(url_for('dok.dodaj_dokument', dokument_type=form.rodzaj2.data))
        

    return render_template(
        "dod_dok.html",
        title="SimpleData",
        #user=current_user.imie,
        form2=form,
        typ=dokument_type,
        values=result
    )

        #query = text('SELECT dokumenty.*, kontrahenci.nazwa_firmy FROM dokumenty JOIN kontrahenci ON dokumenty.NIP_kontrahenta = kontrahenci.NIP WHERE dokumenty.NIP_kontrahenta = :nip')
        #values = db.session.execute(query, {'nip': 1234567890})
        #flash(f'Zaktualizowano aktualnie zalogowanego użytkownika. Proszę zalogować się ponownie', 'success')
    #if form.validate_on_submit():
    #    query2 = text("INSERT INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_wykonania, data_waznosci_towaru) VALUES ('12345', '2022-05-11', 1, 1234567890, 'PZ', '2022-05-11', '2022-06-11');")
    #    db.session.execute(query2)
    #    db.session.commit()
    #    query = text('SELECT dokumenty.*, kontrahenci.nazwa_firmy FROM dokumenty JOIN kontrahenci ON dokumenty.NIP_kontrahenta = kontrahenci.NIP WHERE dokumenty.NIP_kontrahenta = :nip')
    #    values = db.session.execute(query, {'nip': 1234567890})
    #    flash(f'Zaktualizowano aktualnie zalogowanego użytkownika. Proszę zalogować się ponownie', 'success')

    #return render_template(
    #    "dokumenty.html",
    #    title = "SimpleData",
    #    #user = current_user.imie,
    #    form=form,
    #    values = result
    #)
@dok.route('/dokumenty/towar_dokument<numer_dokumentu>', methods=['GET', 'POST'])
def dodajtowar_dok(numer_dokumentu):
    form = DodajTowarDokument()
    query = text("SELECT d.*, k.* FROM dokumenty d JOIN kontrahenci k ON d.NIP_kontrahenta = k.NIP WHERE d.numer_dokumentu = :numer_dokumentu;;")
    query2 = "SELECT * FROM towary WHERE NIP = :nip"
    query3 = "SELECT td.*, t.* FROM `towary_dokument` td JOIN towary t ON td.id_towaru = t.id_towaru WHERE id_dokumentu = :numer_dokumentu "
    values = db.session.execute(query, {'numer_dokumentu': numer_dokumentu}).fetchall()
    nip= values[0].NIP
    values2 = db.session.execute(text(query3), {"numer_dokumentu": numer_dokumentu}).fetchall()
    values3 = db.session.execute(text(query2), {"nip": nip}).fetchall()
    if form.validate_on_submit():
        towary_dokument = TowaryDokument(
            id_dokumentu=numer_dokumentu,
            id_towaru=form.id_towaru.data,
            ilosc=form.il.data,
            data_waznosci=date.today()  # Pominąłem pole data_waznosci, dodaj odpowiednią wartość
        )

        db.session.add(towary_dokument)
        db.session.commit()
        return redirect(url_for('dok.dodajtowar_dok', numer_dokumentu=numer_dokumentu))
    return render_template(
        "dok.html",
        title="SimpleData",
        #user=current_user.imie,
        form=form,
        values=values,
        values2=values2,
        values3=values3,
        numer = numer_dokumentu
        
    )
@dok.route('/dokumenty/towar_dokument/dodaj<numer_dokumentu><tow><ilosc>', methods=['GET', 'POST'])
def dodaj(numer_dokumentu, tow, ilosc):
    flash("dziala")
    return redirect(url_for('dok.dodajtowar_dok', numer_dokumentu=numer_dokumentu))
@dok.route('/dokumenty/towar_dokument<numer_dokumentu>/str<status>', methods=['GET', 'POST'])
def zakoncz(numer_dokumentu, status):
    query = text("UPDATE dokumenty SET statusd = :status WHERE numer_dokumentu = :numer_dokumentu")
    db.session.execute(query, {'numer_dokumentu': numer_dokumentu,'status': status})
    db.session.commit()
    flash(f"Status dokumentu został zmieniony na {status}.")
    return redirect(url_for('dok.dokumenty'))

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>/finalizuj/str:<typ>', methods=['GET', 'POST'])
def finalizuj(numer_dokumentu, typ):
    if typ=="WZ":
        flash(f"Finalizuj WZ.")
    elif typ=="PZ":
        flash(f"Finalizuj PZ.")
    elif typ=="Usun":
        query = "DELETE FROM towary_dokument WHERE id_dokumentu = :numer_dokumentu"
        db.session.execute(text(query), {"numer_dokumentu": numer_dokumentu})
        query = "DELETE FROM dokumenty WHERE numer_dokumentu = :numer_dokumentu"
        db.session.execute(text(query), {"numer_dokumentu": numer_dokumentu})
        db.session.commit()
        flash('Dokument został anulowany')
    return redirect(url_for('dok.dokumenty'))
