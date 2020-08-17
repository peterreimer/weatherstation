import json
import os
from flask import Blueprint
from flask import current_app
from flask import send_file


bp = Blueprint("raw", __name__)

@bp.route("/raw", methods=["GET"])
def latest_measurements():
    return send_file(current_app.config['RAW'])
