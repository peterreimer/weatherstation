import json
import os
from flask import Flask, jsonify, send_file, request

def si_conversion(params):
    """Convert to proper SI units"""
    conversions = {
        'indoortempf': f2c,
        'tempf': f2c,
        'dewptf': f2c,
        'windchillf': f2c,
        'windspeedmph': m2k,
        'windgustmph': m2k,
        'absbaromin': i2h,
        'baromin': i2h,
        'rainin': i2m,
        'dailyrainin': i2m,
        'weeklyrainin': i2m,
        'monthlyrainin': i2m,
        'yearlyrainin': i2m,
        'indoorhumidity': make_float,
        'humidity': make_float,
        'solarradiation': make_float,
        'UV': make_float,
        'winddir': make_float,
        }
    params_si = {}
    for key in params.keys():
       if key in conversions.keys():
           params_si[key] = conversions[key](params[key])
       else: 
           params_si[key] = params[key]
    return params_si

def f2c(fahrenheit):
    """Convert Fahrenheit to Celcius"""
    celsius = ( float(fahrenheit) - 32) * 5 / 9 
    return round(celsius,1)

def m2k(miles):
    """Convert mph to kmh"""
    kilometer = float(miles) * 1.609344
    return round(kilometer, 1)

def i2h(inHg):
    """Convert inHg to hPa"""
    hPa = 33.8638815789 * float(inHg)
    return round(hPa, 1)

def i2m(inch):
    """Convert inch to mm"""
    mm = 25.4 * float(inch)
    return round(mm, 1)

def make_float(value):
    """Convert to float"""
    return float(value)
