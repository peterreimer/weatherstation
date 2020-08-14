import json
import os
from flask import Blueprint
from flask import send_file

LATEST = 'latest.json'
RAW = 'raw.json'

bp = Blueprint("latest", __name__)

@bp.route("/latest", methods=["GET"])
def latest_measurements():
    return send_file(LATEST)
