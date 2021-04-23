#!/usr/bin/env python3
import json
import os
import datetime

import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.plotting import output_file, save
from bokeh.plotting import ColumnDataSource
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, LinearAxis, Range1d



from flask import Blueprint
from flask import render_template
from flask import current_app


bp = Blueprint("index", __name__)

today = datetime.date.today().strftime("%Y%m%d")

@bp.route("/", defaults={"date": today})
@bp.route("/<string:date>")
def weather(date):
    f = open(current_app.config['LATEST'], "r")
    data = json.load(f)
    log_file = logfile_from_date(date)
    #log_file = "~/git/weatherstation/plot/log/2021/03/20210330.csv"
    plot = chart(log_file)
    script, div = components(plot)
    next, previous = next_previous(date)
    return render_template("index.html", date=pretty_date(date), next=next, previous=previous, latest=data, the_div=div, the_script=script)

def chart(log_file):

    df = pd.read_csv(log_file)
    #df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%dT%H:%M:%S")
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    source = ColumnDataSource(df)
    plot_width = 800
    plot_height = 250
    temp_plot = figure(x_axis_type="datetime", y_axis_label="Temperatur")
    
    temp_plot.yaxis.formatter = NumeralTickFormatter(language="de")
    temp_plot.line(x="date", y="temp_outdoor", source=source, legend_label="Temperatur", line_width=2, line_color="red")
    temp_plot.line(x="date", y="temp_dewpoint", source=source, legend_label="Taupunkt", line_width=2)
    
    precipitation_plot = figure(x_axis_type="datetime", y_axis_label="Regenrate [mm/h]")
    precipitation_plot.yaxis.formatter = NumeralTickFormatter(language="de")
    precipitation_plot.line(x="date", y="rain_rate", source=source, legend_label="Regenrate", line_width=2, line_color="blue")
    precipitation_plot.extra_y_ranges = {"y2":Range1d(0,20)}
    precipitation_plot.add_layout(LinearAxis(y_range_name = "y2"), 'right')
    precipitation_plot.line(x="date", y="rain_daily", source=source, legend_label="Regenmenge", line_width=2, line_color="green", y_range_name = "y2")
    
    wind_plot = figure(x_axis_type="datetime", y_axis_label="Regenrate [mm/h]")
    wind_plot.yaxis.formatter = NumeralTickFormatter(language="de")
    wind_plot.line(x="date", y="wind_speed", source=source, legend_label="Windgeschwindigkeit", line_width=2, line_color="blue")
    wind_plot.line(x="date", y="wind_gust", source=source, legend_label="Windböen", line_width=2, line_color="green")
    wind_plot.extra_y_ranges = {"y2":Range1d(0,360)}
    wind_plot.add_layout(LinearAxis(y_range_name = "y2"), 'right')
    wind_plot.line(x="date", y="wind_direction", source=source, legend_label="Windrichtung", line_width=2, line_color="red", y_range_name = "y2")

    pressure_plot = figure(x_axis_type="datetime", y_axis_label="rel. Luftdruck [hPa]")
    pressure_plot.line(x="date", y="pressure_rel", source=source, legend_label="relativer Luftdruck", line_width=2, line_color="blue")
    
    humidity_plot = figure(x_axis_label="Uhrzeit", x_axis_type="datetime", y_axis_label="Luftfeuchtigkeit [%]")
    humidity_plot.line(x="date", y="humidity_outdoor", source=source, legend_label="Luftfeuchtigkeit", line_width=2, line_color="blue")
    humidity_plot.xaxis.formatter = DatetimeTickFormatter(hours = ['%H:%M h'])

    sun_plot = figure(x_axis_type="datetime", y_axis_label="Sonnenstrahlung [W/m²]")
    sun_plot.line(x="date", y="solarradiation", source=source, legend_label="Sonnenstrahlung", line_width=2, line_color="yellow")
    sun_plot.extra_y_ranges = {"y2":Range1d(0,12)}
    sun_plot.add_layout(LinearAxis(y_range_name = "y2"), 'right')
    sun_plot.line(x="date", y="uv_index", source=source, legend_label="UV Index", line_width=2, line_color="orange", y_range_name = "y2")


    #return column(temp_plot, precipitation_plot)
    return gridplot([temp_plot, precipitation_plot, wind_plot, pressure_plot, humidity_plot, sun_plot], ncols=1, plot_width=plot_width, plot_height=plot_height, )

def next_previous(date):
    current = datetime.datetime.strptime(date, "%Y%m%d")
    next = current + datetime.timedelta(days=1)
    today = datetime.date.today().strftime("%Y%m%d")
    previous = current - datetime.timedelta(days=1)
    return next.strftime("%Y%m%d"), previous.strftime("%Y%m%d")

def logfile_from_date(date):
    current = datetime.datetime.strptime(date, "%Y%m%d")
    year = current.strftime("%Y")
    month = current.strftime("%m")
    logfile = os.path.join(current_app.instance_path, year, month, date + ".csv")
    return logfile

def pretty_date(date):
    current = datetime.datetime.strptime(date, "%Y%m%d")
    return current.strftime("%A, %d. %B %Y")


if __name__ == "__main__":

    
    plot = chart("/home/peter/git/weatherstation/instance/2021/04/20210420.csv")
    output_file(filename="/home/peter/public_html/wetterplot.html", title="Wetterdaten")
    save(plot)

    print(pretty_date("19720301"))
    print(next_previous("19720301"))
    
