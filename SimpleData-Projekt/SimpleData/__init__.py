# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = "e761d6362a5b7811a2b1a7e227e39900"

import SimpleData.views

