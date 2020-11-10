#import functools
import json
import os
import csv

from datetime import datetime

from flask import Blueprint
from flask import current_app
#from flask import redirect
#from flask import render_template
from flask import request
#from flask import session
#from flask import url_for
#from flask import jsonify
#from flask import send_file

from weatherstation.conversions import si_conversion

bp = Blueprint("add", __name__)

@bp.route("/add", methods=["GET"])
def add():
    """Receives data from the weatherstation and writes it to disk."""

    raw_data = request.args
    si = si_conversion(raw_data)
    f = open(current_app.config['LATEST'], "w")
    f.write(json.dumps(si))
    f.close
    f = open(current_app.config['RAW'], "w")
    f.write(json.dumps(raw_data))
    f.close
    log(si)
    return "data received"

def log(si):
    dateobj = datetime.fromisoformat(si["date"])
    year = dateobj.strftime("%Y")
    month = dateobj.strftime("%m")
    day = dateobj.strftime("%d")

    csv_daily = "%s%s%s.csv" % (year, month, day)
    data_dir = os.path.join(current_app.instance_path, year, month)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    csv_file = os.path.join(data_dir, csv_daily)
    # add header only when we start a new file on new day
    add_header = False
    if not os.path.isfile(csv_file):
        add_header = True
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = si.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if add_header is True:
            writer.writeheader()
        writer.writerow(si)

    return "verz erstellt"
