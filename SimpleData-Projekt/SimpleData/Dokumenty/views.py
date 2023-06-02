from flask import Blueprint, render_template, redirect, url_for, flash, request
from SimpleData import db, roles_required
from SimpleData.Dokumenty.forms import  Dok, DodajDokumentForm, DodajTowarDokument  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import Kontrahenci, TowaryDokument, MagazynTowar
from sqlalchemy import text
from flask_login import login_required, current_user
from datetime import date

dok = Blueprint('dok', __name__)
#Tworzymy ścierzkę dostępu którą bedzie można wpisać w wierszu przeglądaraki oraz metody jakie będzie mogła strona wysłać do serwera
@dok.route('/dokumenty', methods=['GET', 'POST'])
@login_required
def dokumenty():
    form = Dok()
    query = text("SELECT * FROM dokumenty WHERE statusd = '' ;")
    result = db.session.execute(query)
    #Po naciśnięciu przysku formularza na stronie nastąpi sprawdzenie poprawności pól oraz wykonanie poniższego kodu jeśli pola są poprawnie wypełnione
    if form.validate_on_submit():
        # Tworzenie zapytania SQL
        query = 'SELECT d.*, k.nazwa_firmy, u.imie, k.NIP FROM dokumenty d JOIN kontrahenci k ON d.id_kon = k.id_kon JOIN uzytkownicy u ON d.id_uzytkownika = u.id'
    
        # Filtry do zastosowania w zapytaniu
        filters = {
            'numer_dokumentu': 'd.numer_dokumentu = :numer_dokumentu',
            'data_wystawienia': 'd.data_wystawienia = :data_wystawienia',
            'id_uzytkownika': 'd.id_uzytkownika = :id_uzytkownika',
            'id_kon': 'd.id_kon = :id_kon',
            'typ_dokumentu': 'd.typ_dokumentu = :typ_dokumentu',
            'data_przyjecia': 'd.data_przyjecia = :data_przyjecia',
            'statusd': 'd.statusd = :statusd'
        }
    
        conditions = []  # Lista warunków do zastosowania w zapytaniu
        params = {}  # Słownik przechowujący wartości parametrów

        # Iteracja przez pola formularza i tworzenie warunków oraz parametrów
        for field, condition in filters.items():
            if getattr(form, field).data:
                conditions.append(condition)
                params[field] = getattr(form, field).data
    
        if conditions:
            # Dodanie warunków do zapytania
            query += ' AND ' + ' AND '.join(conditions)
    
        # Wykonanie zapytania z uwzględnieniem parametrów
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
#Niestandardowe sprawdzenie dosepu do strony, wymaganie to użykownik musi być zalogowany oraz posiadać odpowiednie uprawnienia
@roles_required('Administrator','Kierownik')
def dodaj_dokument(dokument_type):
    #Dopisanie do pola formularza jego odpowiedni typ
    if dokument_type == 'PZ':
        form = DodajDokumentForm(rodzaj2='PZ')
    elif dokument_type == 'WZ':
        kontrahenci = Kontrahenci.query.filter_by(status='Odbiorca', stan="Aktywny").all()  # Pobierz odpowiednich kontrahentów z bazy danych
        form = DodajDokumentForm(rodzaj2='WZ', kontrahent2=kontrahenci)

    query = text('SELECT d.*, k.nazwa_firmy, k.NIP FROM dokumenty d JOIN kontrahenci k ON d.id_kon = k.id_kon WHERE d.statusd = "Edycja"')
    result = db.session.execute(query)
    if form.validate_on_submit() and request.method == 'POST':
        rodzaj = dokument_type
        numer = form.numer_dok2.data
        wys = form.data_wys2.data
        nip = form.nip2.data
        kontrahent = Kontrahenci.query.filter_by(NIP=nip, stan="Aktywny").first()  # Sprawdź istnienie kontrahenta
        status = 'Edycja'
        query = text('INSERT INTO dokumenty (numer_dokumentu, data_wystawienia, id_uzytkownika, id_kon, typ_dokumentu, statusd, imie_uzytkownika) VALUES (:numer, :wys, :id_uzytkownika, :id_kon, :rodzaj, :status, :imie_uzy)')
        params = {
            'numer': numer,
            'wys': wys,
            'id_uzytkownika': current_user.id,
            'id_kon': kontrahent.id_kon,
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
        user=current_user.imie,
        form2=form,
        typ=dokument_type,
        values=result
    )
@dok.route('/dokumenty/towar_dokument/<numer_dokumentu>/ok<id_w_towa>', methods=['GET', 'POST'])
@roles_required('Administrator','Kierownik')
def cofnij(numer_dokumentu, id_w_towa):
    towar_do_usuniecia = TowaryDokument.query.get(id_w_towa)
    if towar_do_usuniecia:
        # Usuń rekord z bazy danych
        db.session.delete(towar_do_usuniecia)
        db.session.commit()
    return redirect(url_for('dok.dodajtowar_dok',numer_dokumentu=numer_dokumentu))

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>', methods=['GET', 'POST'])
@login_required
def dodajtowar_dok(numer_dokumentu):
    form = DodajTowarDokument()
    #POBIERANIE DANYCH O DOKUMENCIE I KONTRAHENCIE
    query = text("SELECT d.*, k.* FROM dokumenty d JOIN kontrahenci k ON d.id_kon = k.id_kon WHERE d.numer_dokumentu = :numer_dokumentu;;")
    values = db.session.execute(query, {'numer_dokumentu': numer_dokumentu}).fetchall()
    nip= values[0].NIP

    #POBIERANIE DANYCH O TOWARACH W DOKUMENCIE
    query2 = "SELECT td.*, t.* FROM `towary_dokument` td JOIN towary t ON td.id_towaru = t.id_towaru WHERE id_dokumentu = :numer_dokumentu "
    values2 = db.session.execute(text(query2), {"numer_dokumentu": numer_dokumentu}).fetchall()

    #POBIERANIE DANYCH W ZALEŻNOŚCI ALBO Z TOWARÓW ALBO Z MAGAZYNU
    if values[0].typ_dokumentu=='PZ':
        query3 = "SELECT * FROM towary WHERE NIP = :nip AND stan='Aktywna'"
        values3 = db.session.execute(text(query3), {"nip": nip}).fetchall()
    elif values[0].typ_dokumentu=='WZ':
        query3 = "SELECT DISTINCT mg.id_towaru, mg.idmag, COUNT(*) AS stan, t.* FROM magazyn_towar mg JOIN towary t ON mg.id_towaru = t.id_towaru WHERE mg.stan='Przyjete' GROUP BY mg.id_towaru;"
        values3 = db.session.execute(text(query3)).fetchall()

    if form.validate_on_submit():
        if values[0].typ_dokumentu == 'PZ':
            # Dodawanie towaru do dokumentu typu PZ
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
            # Walidacja, czy wprowadzona ilość towarów nie przekracza dostępnej ilości na magazynie
            flash("Wprowadziłeś większą ilość towarów niż liczba towarów na magazynie")
            return redirect(url_for('dok.dodajtowar_dok', numer_dokumentu=numer_dokumentu))
        else:
            # Dodawanie towarów do dokumentu innego typu niż PZ
            numery = db.session.execute(
                text('SELECT idmag FROM magazyn_towar WHERE id_towaru = :num ORDER BY data_przyjecia ASC'),
                {'num': form.id_towaru.data}
            ).fetchall()
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
        user=current_user.imie,
        form=form,
        values=values,
        values2=values2,
        values3=values3,
        numer = numer_dokumentu
    )

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>/str<status>', methods=['GET', 'POST'])
@login_required
def zakoncz(numer_dokumentu, status):
    query = text("UPDATE dokumenty SET statusd = :status WHERE numer_dokumentu = :numer_dokumentu")
    db.session.execute(query, {'numer_dokumentu': numer_dokumentu,'status': status})
    db.session.commit()
    flash(f"Status dokumentu został zmieniony na {status}.")
    return redirect(url_for('dok.dokumenty'))

@dok.route('/dokumenty/towar_dokument<numer_dokumentu>/finalizuj/<typ>', methods=['GET', 'POST'])
@roles_required('Administrator','Kierownik','Pracownik')
def finalizuj(numer_dokumentu, typ):
    query5=text("UPDATE dokumenty SET statusd = 'Zakończona', data_przyjecia=:data WHERE numer_dokumentu = :num")

    #FINALIZUJ WZ
    if typ=="WZ":
        query=text("UPDATE magazyn_towar SET stan='Wydane' WHERE idmag IN (SELECT numer_towaru from towary_dokument where id_dokumentu=:num);")
        db.session.execute(query, {'num':numer_dokumentu})
        db.session.execute(query5, {"num": numer_dokumentu, "data": date.today()})
        db.session.commit()

    #FINALIZUJ PZ
    elif typ == "PZ":
        # Pobranie informacji o ilości towarów w dokumencie
        query = text("SELECT id_towaru, ilosc, (SELECT SUM(ilosc) FROM towary_dokument WHERE id_dokumentu= :num) liczba FROM `towary_dokument` WHERE id_dokumentu= :num")
        values = db.session.execute(query, {"num": numer_dokumentu}).fetchall()
        j = 1
        # Pobranie informacji o dostępnej pojemności magazynu
        query = text("SELECT COUNT(*) AS suma FROM magazyn_towar WHERE 1")
        suma_towarow = db.session.execute(query).scalar()
        query_pojemnosc = text("SELECT SUM(pojemnosc_sekcji), max(nr_sekcji) as nr_sekcji FROM sekcja")
        magazyn = db.session.execute(query_pojemnosc).scalar()
        magazyn = magazyn - suma_towarow
        k = 0
        if values[0].liczba <= magazyn:
            sekcja = db.session.execute(query_pojemnosc).fetchone()
            for item in values:
                for i in range(int(item.ilosc)):
                    # Pobranie numeru sekcji, która ma wystarczającą pojemność
                    query2 = text("SELECT s.nr_sekcji FROM sekcja s WHERE pojemnosc_sekcji > (SELECT COUNT(*) FROM magazyn_towar WHERE nr_sekcji = :nr) AND nr_sekcji = :nr2")
                    numer = db.session.execute(query2, {'nr': j, 'nr2': j}).fetchone()
                    while numer is None:
                        j += 1
                        numer = db.session.execute(query2, {'nr': j, 'nr2': j}).fetchone()
                        if j > int(sekcja[1]):
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
            k += 1

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
