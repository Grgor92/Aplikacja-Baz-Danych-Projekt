from flask import Blueprint, render_template
from flask_login import current_user, login_required
from SimpleData import  db
from SimpleData.Magazyn.forms import magazyn_towar
from sqlalchemy import text

mag = Blueprint('mag', __name__)

@mag.route('/magazyn_towar', methods=['GET', 'POST'])
@login_required
def magazyn_towar_t():
    form = magazyn_towar()
    query = 'SELECT DISTINCT magazyn_towar.*, towary.* FROM magazyn_towar JOIN towary ON magazyn_towar.id_towaru = towary.id_towaru WHERE magazyn_towar.stan = "Przyjete";'

    result = db.session.execute(text(query))
    if form.validate_on_submit():
        
        params = {}
        if form.nr_sekcji.data:
            query += 'AND nr_sekcji = :nr_sekcji '
            params['nr_sekcji'] = form.nr_sekcji.data

        if form.data_przyjecia.data:
            query += 'AND data_przyjecia = :data_przyjecia '
            params['data_przyjecia'] = form.data_przyjecia.data

        if form.numer_dokumentu.data:
            query += 'AND numer_dokumentu = :numer_dokumentu '
            params['numer_dokumentu'] = form.numer_dokumentu.data

        if form.NIP.data:
            query += 'AND NIP = :NIP '
            params['NIP'] = form.NIP.data
        if form.typ.data:
            query += 'AND typ = :typ '
            params['typ'] = form.typ.data

        if form.rodzaj.data:
            query += 'AND rodzaj = :rodzaj '
            params['rodzaj'] = form.rodzaj.data

        if form.nazwa.data:
            query += 'AND nazwa = :nazwa '
            params['nazwa'] = form.nazwa.data


        query = text(query)
        result = db.session.execute(query, params)
        db.session.commit()
    return render_template(
        "magazyn_towar.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form,
        values=result
    )
