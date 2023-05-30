from flask import Blueprint, jsonify, render_template, url_for, redirect
from datetime import datetime
from flask_login import current_user, login_required, logout_user
from SimpleData import  db, bcrypt, app
from SimpleData.Magazyn.forms import magazyn_towar
from sqlalchemy import inspect, text
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from SimpleData.tabele import uzytkownicy

mag = Blueprint('mag', __name__)

@mag.route('/magazyn_towar', methods=['GET', 'POST'])
@login_required
def magazyn_towar_t():
    form = magazyn_towar()
    return render_template(
        "magazyn_towar.html",
        title = "SimpleData",
        user = current_user.imie,
        form=form
    )
