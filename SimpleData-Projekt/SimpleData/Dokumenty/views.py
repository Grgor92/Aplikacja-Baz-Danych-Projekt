
from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request
from SimpleData import app, db
from SimpleData.Dokumenty.forms import  Dok, DodajDokumentForm, DodajTowarDokument  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import uzytkownicy, Kontrahenci, dokumenty, TowaryDokument, MagazynTowar
from sqlalchemy import text
from flask_login import login_required, current_user, fresh_login_required
from datetime import date

dok = Blueprint('dok', __name__)

@dok.route('/dokumenty', methods=['GET', 'POST'])
#@login_required
def dokumenty():
    form = Dok()
    query = text("SELECT * FROM dokumenty WHERE statusd = '' ;")
    result = db.session.execute(query)
    query3 = text("INSERT IGNORE INTO kontrahenci (NIP, nazwa_firmy, miasto, telefon, ulica, numer, status) VALUES ('1234567890', 'Galicjanka', 'Galicja', 512512512, 'Galicyjska', '54A', 'Dostawca');")
    db.session.execute(query3)
    query2 = text("INSERT IGNORE INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, data_przyjecia,  statusd) VALUES ('12345', '2022-05-11', :user_id, 1234567890, 'PZ', '2022-05-11', 'Aktywna');")
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
            'data_przyjecia': 'd.data_przyjecia = :data_przyjecia',
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
        user = current_user.imie,
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
        status = 'Edycja'
        query = text('INSERT INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, NIP_kontrahenta, typ_dokumentu, statusd, imie_uzytkownika) VALUES (:numer, :wys, :id_uzytkownika, :nip, :rodzaj, :status, :imie_uzy)')
        params = {
            'numer': numer,
            'wys': wys,
            'id_uzytkownika': current_user.id,
            'nip': nip,
            'rodzaj': rodzaj,
            'status': status,
            'imie_uzy': current_user.imie
        }
        db.session.execute(query, params)
        db.session.commit()
        flash('Dokument został dodany') 
        return redirect(url_for('dok.dodaj_dokument', dokument_type=form.rodzaj2.data))

    return render_template(
        "dod_dok.html",
        title="SimpleData",
        #user=current_user.imie,
        form2=form,
        typ=dokument_type,
        values=result
    )
@dok.route('/dokumenty/towar_dokument/<numer_dokumentu>/ok<id_w_towa>', methods=['GET', 'POST'])
def cofnij(numer_dokumentu, id_w_towa):
    towar_do_usuniecia = TowaryDokument.query.get(id_w_towa)
    if towar_do_usuniecia:
        # Usuń rekord z bazy danych
        db.session.delete(towar_do_usuniecia)
        db.session.commit()
    return redirect(url_for('dok.dodajtowar_dok',numer_dokumentu=numer_dokumentu))

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>', methods=['GET', 'POST'])
def dodajtowar_dok(numer_dokumentu):
    form = DodajTowarDokument()
    #POBIERANIE DANYCH O DOKUMENCIE I KONTRAHENCIE
    query = text("SELECT d.*, k.* FROM dokumenty d JOIN kontrahenci k ON d.NIP_kontrahenta = k.NIP WHERE d.numer_dokumentu = :numer_dokumentu;;")
    values = db.session.execute(query, {'numer_dokumentu': numer_dokumentu}).fetchall()
    nip= values[0].NIP

    #POBIERANIE DANYCH O TOWARACH W DOKUMENCIE
    query2 = "SELECT td.*, t.* FROM `towary_dokument` td JOIN towary t ON td.id_towaru = t.id_towaru WHERE id_dokumentu = :numer_dokumentu "
    values2 = db.session.execute(text(query2), {"numer_dokumentu": numer_dokumentu}).fetchall()

    #POBIERANIE DANYCH W ZALEŻNOŚCI ALBO Z TOWARÓW ALBO Z MAGAZYNU
    if values[0].typ_dokumentu=='PZ':
        query3 = "SELECT * FROM towary WHERE NIP = :nip"
        values3 = db.session.execute(text(query3), {"nip": nip}).fetchall()
    elif values[0].typ_dokumentu=='WZ':
        query3 = "SELECT DISTINCT mg.id_towaru, mg.idmag, COUNT(*) AS stan, t.* FROM magazyn_towar mg JOIN towary t ON mg.id_towaru = t.id_towaru WHERE mg.stan='Przyjete' GROUP BY mg.id_towaru;;"
        values3 = db.session.execute(text(query3)).fetchall()

    if form.validate_on_submit():
            if values[0].typ_dokumentu=='PZ':
                towary_dokument = TowaryDokument(
                    id_dokumentu=numer_dokumentu,
                    id_towaru=form.id_towaru.data,
                    ilosc=form.il.data,
                    data_przyjecia=date.today()
                    )
                db.session.add(towary_dokument)
                db.session.commit()
                return redirect(url_for('dok.dodajtowar_dok', numer_dokumentu=numer_dokumentu))
            elif form.il.data > form.il_mag.data:
                flash("Wprwoadziłeś wiekszą ilość toawrów niż liczba towarów na magazynie")
                return redirect(url_for('dok.dodajtowar_dok', numer_dokumentu=numer_dokumentu))
            else:
                numery=db.session.execute(text('SELECT idmag FROM magazyn_towar WHERE id_towaru = :num ORDER BY data_przyjecia ASC'),{'num':form.id_towaru.data}).fetchall()
                for i in range(form.il.data):
                    towary_dokument = TowaryDokument(
                        id_dokumentu=numer_dokumentu,
                        id_towaru=form.id_towaru.data,
                        numer_towaru=numery[i].idmag,
                        ilosc=1,
                        data_przyjecia=date.today()
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

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>/str<status>', methods=['GET', 'POST'])
def zakoncz(numer_dokumentu, status):
    query = text("UPDATE dokumenty SET statusd = :status WHERE numer_dokumentu = :numer_dokumentu")
    db.session.execute(query, {'numer_dokumentu': numer_dokumentu,'status': status})
    db.session.commit()
    flash(f"Status dokumentu został zmieniony na {status}.")
    return redirect(url_for('dok.dokumenty'))

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>/finalizuj/<typ>', methods=['GET', 'POST'])
def finalizuj(numer_dokumentu, typ):
    #FINALIZUJ WZ
    if typ=="WZ":
        flash(f"Finalizuj WZ.")




    #FINALIZUJ PZ
    elif typ=="PZ":
        query = text("SELECT id_towaru, ilosc, (SELECT SUM(ilosc) from towary_dokument where id_dokumentu= :num) liczba FROM `towary_dokument` where id_dokumentu= :num")
        values = db.session.execute(query, {"num": numer_dokumentu}).fetchall()
        j=1;
        query = text("SELECT COUNT(*) AS suma FROM magazyn_towar WHERE 1")
        suma_towarow = db.session.execute(query).scalar()
        query_pojemnosc = text("SELECT SUM(pojemnosc_sekcji), max(nr_sekcji) as nr_sekcji FROM sekcja")
        magazyn = db.session.execute(query_pojemnosc).scalar()
        magazyn=magazyn-suma_towarow
        k=0
        if values[0].liczba <= magazyn:
            for item in values:
                for i in range(int(item.ilosc)):
                    query2 = text("SELECT s.nr_sekcji FROM sekcja s WHERE pojemnosc_sekcji > (SELECT COUNT(*) FROM magazyn_towar WHERE nr_sekcji = :nr) AND nr_sekcji = :nr2")
                    numer=db.session.execute(query2, {'nr':j, 'nr2':j }).fetchone()
                    while numer == None:
                        j=j+1
                        numer=db.session.execute(query2, {'nr':j, 'nr2':j }).fetchone()
                        if j>int(magazyn[0].nr_sekcji):
                            break
                    magazyn_towar = MagazynTowar(
                        nr_sekcji=numer.nr_sekcji,  # Dodaj właściwy numer sekcji
                        data_przyjecia=date.today(),  # Dodaj właściwą datę przyjęcia
                        id_towaru=int(item.id_towaru),
                        numer_dokumentu=numer_dokumentu,
                        stan="Przyjete"
                    )
                    db.session.add(magazyn_towar)
                    db.session.commit()
            k=k+1
            query5=text("UPDATE dokumenty SET statusd = 'Zakończona', data_przyjecia=:data WHERE numer_dokumentu = :num")
            db.session.execute(query5, {"num": numer_dokumentu, "data": date.today()})
            db.session.commit()
        else:
            flash("Ilość towarów przekracza dostępną pojemność magazynu.", 'danger')
    #USUŃ DOKUMENT W TRAKCIE EDYCJI
    elif typ=="Usun":
        query = "DELETE FROM towary_dokument WHERE id_dokumentu = :numer_dokumentu"
        db.session.execute(text(query), {"numer_dokumentu": numer_dokumentu})
        query = "DELETE FROM dokumenty WHERE numer_dokumentu = :numer_dokumentu"
        db.session.execute(text(query), {"numer_dokumentu": numer_dokumentu})
        db.session.commit()
        flash('Dokument został anulowany')
    return redirect(url_for('dok.dokumenty'))
