# -*- coding: utf-8 -*-
from multiprocessing.connection import Connection
from asyncio.windows_events import NULL
from flask import render_template, jsonify, redirect, url_for, flash, session, request, Flask
from SimpleData import app, db, bcrypt, LoginManager
from datetime import datetime
from .forms import RegistrationForm, LoginForm, przeszukiwanie_d, dok_historyczne, kontrahenci_F, uzytkownicy, magazyn_towar, Users_zmiana, moje_ustawienia, DodajDokumentForm  # import z innego pliku w tym samym miejscu musi zawierać . przed nazwą
from SimpleData import db, bcrypt
from SimpleData.tabele import Uzytkownicy, Kontrahenci, Dokumenty
from sqlalchemy import inspect, text
from flask_login import login_user, logout_user, login_required, current_user, fresh_login_required
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash













