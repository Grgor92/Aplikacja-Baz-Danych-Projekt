from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from SimpleData.Kontrahenci.forms import kontrahenci_F  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db, roles_required
from SimpleData.tabele import Kontrahenci
from sqlalchemy import text
from flask_login import login_required, current_user, fresh_login_required

kon = Blueprint('kon', __name__)

@kon.route('/kontrahenci', methods=['GET', 'POST'])
@login_required
def kontrahenci_t():
    form = kontrahenci_F()
    values=Kontrahenci.query.filter_by(stan="Aktywny")
    if request.method == 'POST':
        nip = request.form.get('nip')
        nazwa_firmy = request.form.get('nazwa_firmy')

        if nip and nazwa_firmy:
            kontrahenci = Kontrahenci.query.filter_by(NIP=nip, nazwa_firmy=nazwa_firmy, stan="Aktywny").all()
        elif nip:
            kontrahenci = Kontrahenci.query.filter_by(NIP=nip, stan="Aktywny").all()
        elif nazwa_firmy:
            kontrahenci = Kontrahenci.query.filter_by(nazwa_firmy=nazwa_firmy, stan="Aktywny").all()
        else:
            kontrahenci = Kontrahenci.query.filter_by(stan="Aktywny")

        return render_template('kontrahenci.html', kontrahenci=kontrahenci)


    return render_template('kontrahenci.html', kontrahenci=values, title="SimpleData", user=current_user.imie, form=form)

@kon.route('/dodaj_rekord', methods=['POST'])
@roles_required('Administrator')
def dodaj_rekord():
    nip = request.form.get('nip')
    nazwa_firmy = request.form.get('nazwa_firmy')
    miasto = request.form.get('miasto')
    nr_telefonu = request.form.get('nr_telefonu')
    ulica = request.form.get('ulica')
    numer = request.form.get('numer')
    rodzaj = request.form.get('rodzaj')
    stan = "Aktywny"
    kontrahent = Kontrahenci(NIP=nip, nazwa_firmy=nazwa_firmy, miasto=miasto, telefon=nr_telefonu, ulica=ulica, numer=numer, status=rodzaj, stan=stan)

    db.session.add(kontrahent)
    flash(f'Nowy kontrahent został utworzony.{nip}', 'success')
    db.session.commit()
    return redirect(url_for('kon.kontrahenci_t'))

@kon.route('/kontrahenci/edytuj', methods=['POST'])
@roles_required('Administrator')
def edytuj_kontrahenta():
    #Pobieranie danych z formularza
    edited_nip = request.form['editedField1']
    edited_nazwa_firmy = request.form['editedField2']
    edited_miasto = request.form['editedField3']
    edited_telefon = request.form['editedField4']
    edited_ulica = request.form['editedField5']
    edited_numer = request.form['editedField6']
    edited_rodzaj = request.form['editedField7']

   # Oznacz istniejący rekord jako "Nieaktualny"
    query1 = text("UPDATE kontrahenci SET stan=:stan_nieaktualny WHERE NIP=:nip AND stan=:stan_aktywny")
    db.session.execute(query1, {'stan_nieaktualny': 'Nieaktualny', 'nip': edited_nip, 'stan_aktywny': 'Aktywny'})
    db.session.commit()

    # Stwórz nowy rekord z aktualizowanymi wartościami i stanem "Aktywny"
    query2 = text("INSERT INTO kontrahenci (NIP, nazwa_firmy, miasto, telefon, ulica, numer, status, stan) VALUES (:nip, :nazwa_firmy, :miasto, :telefon, :ulica, :numer, :status, :stan_aktywny)")
    db.session.execute(query2, {'nip': edited_nip, 'nazwa_firmy': edited_nazwa_firmy, 'miasto': edited_miasto, 'telefon': edited_telefon, 'ulica': edited_ulica, 'numer': edited_numer, 'status': edited_rodzaj, 'stan_aktywny': 'Aktywny'})
    db.session.commit()

    flash('Dane kontrahenta zostały zaktualizowane')
    return redirect(url_for('kon.kontrahenci_t'))



@kon.route('/kontrahenci/<string:nip>', methods=['DELETE'])
@roles_required('Administrator')
def delete_kontrahent(nip):
    #Ustawianie obenego kontrahenta na stan nieakutalny
    kontrahent = Kontrahenci.query.filter_by(NIP=nip, stan="Aktywny").first()

    if kontrahent:
        kontrahent.stan = "Nieaktualny"
        db.session.commit()
        return jsonify({'message': 'Stan kontrahenta został zmieniony na Nieaktualny.'}), 200
    else:
        return jsonify({'message': 'Kontrahent o podanym NIP i stanie Aktywny nie został znaleziony.'}), 404

