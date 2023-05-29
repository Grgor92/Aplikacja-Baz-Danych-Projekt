from flask import Blueprint, render_template, request, redirect, url_for, flash
from SimpleData.Kontrahenci.forms import kontrahenci_F  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db
from SimpleData.tabele import kontrahenci
from sqlalchemy import text
from flask_login import login_required, current_user, fresh_login_required

kon = Blueprint('kon', __name__)

@kon.route('/kontrahenci', methods=['GET', 'POST'])
@login_required
def kontrahenci_t():
    form = kontrahenci_F()
    values=kontrahenci.query.all()
    if request.method == 'POST':
        nip = request.form.get('nip')
        nazwa_firmy = request.form.get('nazwa_firmy')

        if nip and nazwa_firmy:
            kontrahenci = kontrahenci.query.filter_by(NIP=nip, nazwa_firmy=nazwa_firmy).all()
        elif nip:
            kontrahenci = kontrahenci.query.filter_by(NIP=nip).all()
        elif nazwa_firmy:
            kontrahenci = kontrahenci.query.filter_by(nazwa_firmy=nazwa_firmy).all()
        else:
            kontrahenci = kontrahenci.query.all()

        return render_template('kontrahenci.html', kontrahenci=kontrahenci)
    return render_template('kontrahenci.html', kontrahenci=values,
    title = "SimpleData",
    user = current_user.imie,
    form=form)

@kon.route('/dodaj_rekord', methods=['POST'])
def dodaj_rekord():
    nip = request.form.get('nip')
    nazwa_firmy = request.form.get('nazwa_firmy')
    miasto = request.form.get('miasto')
    nr_telefonu = request.form.get('nr_telefonu')
    ulica = request.form.get('ulica')
    numer = request.form.get('numer')

    kontrahent = kontrahenci(NIP=nip, nazwa_firmy=nazwa_firmy, miasto=miasto, telefon=nr_telefonu, ulica=ulica, numer=numer)
    db.session.add(kontrahent)
    flash('Nowy kontrahent został utworzony.', 'success')
    db.session.commit()


    return redirect(url_for('kon.kontrahenci_t'))
