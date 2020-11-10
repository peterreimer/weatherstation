import json
import os
from flask import Blueprint
from flask import render_template
from flask import current_app


bp = Blueprint("index", __name__)

@bp.route("/")
def weather():
    f = open(current_app.config['LATEST'], "r")
    data = json.load(f)
    return render_template("index.html", latest=data)
