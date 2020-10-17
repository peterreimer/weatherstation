from flask import Blueprint
from flask import current_app
from flask import send_file

bp = Blueprint("latest", __name__)

@bp.route("/latest", methods=["GET"])
def latest_measurements():
    """Return latest measurement"""
    return send_file(current_app.config['LATEST'])
