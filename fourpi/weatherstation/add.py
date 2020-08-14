import functools
import json
from fourpi.weatherstation.conversions import si_conversion

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from flask import send_file

LATEST = 'latest.json'
RAW = 'raw.json'

bp = Blueprint("add", __name__)

@bp.route("/add", methods=["GET"])
def add():
    print(dir(bp))
    raw_data = request.args
    si = si_conversion(raw_data)
    f = open(LATEST, "w")
    f.write(json.dumps(si))
    f.close
    f = open(RAW, "w")
    f.write(json.dumps(raw_data))
    f.close
    return "data received"
