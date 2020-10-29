import json
import os
from flask import Blueprint
from flask import render_template
from flask import current_app


bp = Blueprint("index", __name__)

@bp.route("/")
def weather():
    return render_template("index.html", last_measurement="heute")
