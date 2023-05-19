from flask import Blueprint, render_template, redirect, url_for, flash, session, request, Flask
from SimpleData import app, db 
from SimpleData.Towary.forms import DodajDokumentForm  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty
from sqlalchemy import inspect, text
from flask_login import login_required, current_user, fresh_login_required

tow = Blueprint('tow', __name__)

@tow.route('/towar', methods=['GET', 'POST'])
@login_required
def towary():
    # dodaj formularz form = kontrahenci()
    #wyrenderuj strone ze wzoru
    return render_template( 
        "towar.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        #form=form
    )

@tow.route('/wypis-towary', methods=['GET', 'POST'])
@login_required
def wypis_towary():
    # dodaj formularz form = kontrahenci()
    #wyrenderuj strone ze wzoru
    return render_template( 
        "wypis_towary.html",
        title = "SimpleData",
        user = current_user.imie, #current_user - dane użytkownika, imie - krotka do której chcemy dostęp
        #form=form
    )