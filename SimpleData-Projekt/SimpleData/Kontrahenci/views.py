from flask import Blueprint, render_template, request, redirect, url_for, flash
from SimpleData.Kontrahenci.forms import kontrahenci_F  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db
from SimpleData.tabele import Kontrahenci
from sqlalchemy import text
from flask_login import login_required, current_user, fresh_login_required

kon = Blueprint('kon', __name__)

@kon.route('/kontrahenci', methods=['GET', 'POST'])
@login_required
def kontrahenci_t():
    form = kontrahenci_F()
    values = Kontrahenci.query.all()

    if request.method == 'POST':
        nip = request.form.get('nip')
        nazwa_firmy = request.form.get('nazwa_firmy')

        if nip and nazwa_firmy:
            kontrahenci = Kontrahenci.query.filter_by(NIP=nip, nazwa_firmy=nazwa_firmy).all()
        elif nip:
            kontrahenci = Kontrahenci.query.filter_by(NIP=nip).all()
        elif nazwa_firmy:
            kontrahenci = Kontrahenci.query.filter_by(nazwa_firmy=nazwa_firmy).all()
        else:
            kontrahenci = Kontrahenci.query.all()

        return render_template('kontrahenci.html', kontrahenci=kontrahenci)

    if request.method == 'GET' and 'editedField1' in request.args:
        nip = request.args.get('editedField1')
        nazwa_firmy = request.args.get('editedField2')
        miasto = request.args.get('editedField3')
        nr_telefonu = request.args.get('editedField4')
        ulica = request.args.get('editedField5')
        numer = request.args.get('editedField6')

        kontrahent = Kontrahenci.query.filter_by(NIP=nip).first()
        if kontrahent:
            kontrahent.nazwa_firmy = nazwa_firmy
            kontrahent.miasto = miasto
            kontrahent.telefon = nr_telefonu
            kontrahent.ulica = ulica
            kontrahent.numer = numer
            db.session.commit()
            flash('Kontrahent został zaktualizowany.', 'success')
        else:
            flash('Kontrahent nie został znaleziony.', 'error')

        return redirect(url_for('kon.kontrahenci_t'))

    return render_template('kontrahenci.html', kontrahenci=values, title="SimpleData", user=current_user.imie, form=form)


@kon.route('/dodaj_rekord', methods=['POST'])
def dodaj_rekord():
    nip = request.form.get('nip')
    nazwa_firmy = request.form.get('nazwa_firmy')
    miasto = request.form.get('miasto')
    nr_telefonu = request.form.get('nr_telefonu')
    ulica = request.form.get('ulica')
    numer = request.form.get('numer')

    kontrahent = Kontrahenci(NIP=nip, nazwa_firmy=nazwa_firmy, miasto=miasto, telefon=nr_telefonu, ulica=ulica, numer=numer)
    db.session.add(kontrahent)
    flash('Nowy kontrahent został utworzony.', 'success')
    db.session.commit()


    return redirect(url_for('kon.kontrahenci_t'))
