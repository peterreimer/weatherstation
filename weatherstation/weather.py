import json
import os
from flask import Blueprint
from flask import render_template
from flask import current_app


bp = Blueprint("weather", __name__)

@bp.route("/weather")
def weather():
    return render_template("weather.html", last_measurement="heute")
