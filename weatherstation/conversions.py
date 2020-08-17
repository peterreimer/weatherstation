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
        "windchillf": ["temp_windchill", f2c],
        "windspeedmph":["wind_speed", m2k],
        "windgustmph": ["wind_gust", m2k],
        "winddir": ["wind_direction", make_float],
        }
    params_si = collections.OrderedDict()
    for key in conversions.keys():
        new_key = conversions[key][0]
        if key in params.keys():
            #print("old: %s, new: %s value: %s" % (key, new_key, params[key]))
            params_si[new_key] = conversions[key][1](params[key])
    
    # extra: Beauford scale and compass direction of wind
    params_si["wind_compass"] = deg2compass(float(params["winddir"])) 
    params_si["wind_beaufort"] = wind2beaufort(float(params["windspeedmph"])) 
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

def deg2compass(degree):
    """https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words/7490772#7490772"""
    val = int(( degree / 22.5 ) + 0.5 )
    arr = ["N","NNO","NO","ONO","O","OSO", "SO", "SSO","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[( val % 16 )]

def mph2beaufort(miles):
    kmh = m2k(miles)
    x = 12
    scale = [1, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117]
    for beaufort, speed in enumerate(scale):
        upper_limit = speed
        if beaufort == 0:
            lower = 0
        else:
            lower = scale[beaufort - 1]
        print(lower, upper))
        if (kmh >= lower) and (kmh < upper):
            x = beaufort
            break
    return x

if __name__ == '__main__':
    
    #for v in [1.2, 8.1, 4.6, 32.2, 64.4]:
    #    print("%s: %s"  % (v, mph2beaufort(v)))
    v = 12
    print("%s: %s"  % (v, mph2beaufort(v)))

