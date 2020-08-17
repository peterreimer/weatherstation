import collections
from datetime import datetime
from datetime import timezone

def si_conversion(params):
    """Convert to proper SI units"""
    conversions = {
        "dateutc": ["date", utc2local],
        "indoortempf": ["temp_indoor", f2c],
        "tempf": ["temp_outdoor", f2c],
        "dewptf": ["temp_dewpoint", f2c],
        "windchillf": ["temp_windchill", f2c],
        "windspeedmph":["wind_speed", m2k],
        "windgustmph": ["wind_gust", m2k],
        "winddir": ["wind_direction", make_float],
        "absbaromin": ["pressure_abs", i2h],
        "baromin": ["pressure_rel", i2h],
        "rainin": ["rain_now", i2m],
        "dailyrainin": ["rain_daily", i2m],
        "weeklyrainin": ["rain_weekly", i2m],
        "monthlyrainin": ["rain_monthly", i2m],
        "yearlyrainin": ["rain_yearly", i2m],
        "indoorhumidity": ["humidity_indoor", make_float],
        "humidity": ["humidity_outdoor", make_float],
        "solarradiation": ["solarradiation", make_float],
        "UV": ["uv_index", make_float],
        }
    params_si = collections.OrderedDict()
    for key in conversions.keys():
        new_key = conversions[key][0]
        if key in params.keys():
            #print("old: %s, new: %s value: %s" % (key, new_key, params[key]))
            params_si[new_key] = conversions[key][1](params[key])
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

def utc2local(utc_string):
    """Convert time give in UTC to more portable local time in iso format""" 
    utc = datetime.strptime(utc_string, "%Y-%m-%d %H:%M:%S")
    local = utc.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return local.isoformat()


if __name__ == '__main__':
    utc = "2020-08-15 13:50:00"
    print(utc2local(utc))
