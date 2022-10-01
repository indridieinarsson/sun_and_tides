#!/usr/bin/env python3
# This file is part of FES library.
#
#  FES is free software: you can redistribute it and/or modify
#  it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FES is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
#  You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#  along with FES.  If not, see <http://www.gnu.org/licenses/>.
"""
Example of using the FES Python interface
"""
import argparse
import numpy as np
import pyfes
import peakutils
from scipy.interpolate import interp1d

# ------------------
import astral
from ics import Calendar, Event
from datetime import datetime, date, timedelta
import pytz
from geopy.geocoders import Nominatim
from functools import partial
from astral.geocoder import database, lookup
from astral.sun import sun

import datetime as dt
from pytz import timezone
from skyfield import almanac
from skyfield.api import E, N, W, wgs84, load

def float_to_datetime(fl):
    return datetime.fromtimestamp(fl)

def usage():
    """
    Command syntax
    """
    parser = argparse.ArgumentParser(
        description='Program example using the Python API for FES.')
    parser.add_argument('ocean',
                        help='Path to the configuration file that contains '
                        'the defintion of grids to use to compute the '
                        'ocean tide',
                        type=argparse.FileType('r'))
    parser.add_argument('load',
                        help='Path to the configuration file that contains '
                        'the defintion of grids to use to compute the '
                        'load tide',
                        type=argparse.FileType('r'))
    parser.add_argument('--startdate',
                        help='Date of calculation of the oceanic tide.', type=datetime.fromisoformat,
                        default=datetime(2021, 5, 1))
    parser.add_argument('--enddate',
                        help='Date of calculation of the oceanic tide.', type=datetime.fromisoformat,
                        default=datetime(2021, 6, 1))

    parser.add_argument('--latitude',
                        help='Latitude.', type=float,
                        default=64.154673)
    parser.add_argument('--longitude',
                        help='Longitude.', type=float,
                        default=-21.908769)
    parser.add_argument('--out',
                        help='Output file.',
                        default="tidal_calendar.ics")
    return parser.parse_args()


def main():
    """
    Main program
    """
    args = usage()

    # Create handler
    short_tide = pyfes.Handler("ocean", "io", args.ocean.name)
    radial_tide = pyfes.Handler("radial", "io", args.load.name)


    delta = args.enddate - args.startdate
    print(delta.days)

    # Creating the time series
    dates = np.array([
        args.startdate + timedelta(seconds=item * 3600/4)
        for item in range((delta.days+1)*24*4)
    ])
    # print("date : ", args.date)
    # print(dates)

    lats = np.full(dates.shape, args.latitude)
    lons = np.full(dates.shape, args.longitude)

    # Stykkishólmur: 65.10761731461221, -22.704729429936798
    #lats = np.full(dates.shape, 65.10761731461221)
    #lons = np.full(dates.shape, -22.704729429936798)

    # Reykjavík:
    #lats = np.full(dates.shape, 64.154673)
    #lons = np.full(dates.shape, -21.908769)

    # Computes tides
    tide, lp, _ = short_tide.calculate(lons, lats, dates)
    t_load, t_load_lp, _ = radial_tide.calculate(lons, lats, dates)

    total_tide = tide + lp + t_load
    t_float = np.array([d.timestamp() for d in dates])
    ttide = interp1d(t_float, total_tide)

    indexes = peakutils.indexes(total_tide, min_dist=4)
    peaks_x = peakutils.interpolate(t_float, total_tide, ind=indexes)
    peaks_x = [float_to_datetime(p) for p in peaks_x]
    flod = list()
    for p in peaks_x:
        p = p.replace(second=0, microsecond=0) 
        try:
            print("%s - flóð %5.2f m " % (p, ttide(p.timestamp())/100 ) )
            flod.append((p, ttide(p.timestamp())/100 ))
        except Exception:
            pass
        

    indexes = peakutils.indexes(-total_tide, min_dist=5*4)
    peaks_x = peakutils.interpolate(t_float, -total_tide, ind=indexes)
    peaks_x = [float_to_datetime(p) for p in peaks_x]
    fjara = list()
    for p in peaks_x:
        p = p.replace(second=0, microsecond=0) 
        try:
            print("%s - fjara %5.2f m " % (p, ttide(p.timestamp())/100 ) )
            fjara.append((p, ttide(p.timestamp())/100 ))
        except Exception:
            pass


    morgun = dict()
    morgun[0] = None
    morgun[1] = "Dögun"
    morgun[2] = None # Nautical Twilight
    morgun[3] = "Birting"
    morgun[4] = "Sólris"
    
    kveld = dict()
    kveld[0] = None
    kveld[1] = "Dagsetur"
    kveld[2] = None # Nautical Twilight
    kveld[3] = "Myrkur"
    kveld[4] = "Sólarlag"
    
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    
    #https://rhodesmill.org/skyfield/examples.html#dark-twilight-day-example
    # 0 Dark of night.
    # 1 Astronomical twilight. - Dögun - Myrkur
    # 2 Nautical twilight.
    # 3 Civil twilight. - Birting - Dagsetur
    # 4 Daytime.
    # def alm_for_day(this_time, city_info, cal):
    def alm_for_day(this_time, lat, lon, cal):
        zone = timezone('UTC')
        now = zone.localize(this_time)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)
        ts = load.timescale()
        t0 = ts.from_datetime(midnight)
        t1 = ts.from_datetime(next_midnight)
        eph = load('de421.bsp')
        # city = wgs84.latlon(city_info.latitude * N, city_info.longitude * E)
        city = wgs84.latlon(lat * N, lon * E)
        f = almanac.dark_twilight_day(eph, city)
        times, events = almanac.find_discrete(t0, t1, f)
        previous_e = f(t0)[()]
        morning_ev = Event()
        morning_ev.name = "Sólarupprás"
        morning_ev.dtstamp = datetime.now()
        morning_desc = ""
        evening_ev = Event()
        evening_ev.name = "Sólsetur"
        evening_ev.dtstamp = datetime.now()
        evening_desc = ""
        for t, e in zip(times, events):
            #print("e ", e)
            tt = t.astimezone(zone)
            tstr = str(t.astimezone(zone))[:16]
            tstr2 = str(t.astimezone(zone))[11:16]
            if previous_e < e:
                if not morgun[e] is None:
                    tmp = "{} {}".format(tstr2, morgun[e])#, 'starts'
                    morning_desc += tmp
                if e == 4: # Day starts:
                    print(tstr, morgun[e])
                    morning_ev.begin = tt
                    morning_ev.duration = timedelta(seconds=10)
                else:
                    pass
            else:
                if not kveld[previous_e] is None:
                    tmp = "{} {}".format(tstr2, kveld[previous_e])#, 'starts'
                    evening_desc += tmp
                if e == 3 : # Day ends
                    evening_ev.begin = tt
                    evening_ev.duration = timedelta(seconds=10)
                else:
                    pass
            previous_e = e
        morning_ev.description = morning_desc
        cal.events.add(morning_ev)
        evening_ev.description = evening_desc
        cal.events.add(evening_ev)
        print(morning_desc)
        print(evening_desc)
    
    cal = Calendar()
    
    citystr = "Reykjavik"
    geolocator = Nominatim(user_agent="indridis_calendar_generator")
    geocode = partial(geolocator.geocode, language="en")
    city_info = geocode(citystr)
    
    start_date = args.startdate#  datetime(2021, 1, 1)
    end_date = args.enddate# datetime(2021, 12, 31)
    for single_date in daterange(start_date, end_date):
        # alm_for_day(single_date, city_info, cal)
        alm_for_day(single_date, args.latitude, args.longitude, cal)

    for f in flod:
        flod_ev = Event()
        flod_ev.name = "Flóð"
        flod_ev.dtstamp = datetime.now()
        flod_ev.description = "%s : %5.2f m" % f 
        flod_ev.begin = f[0]
        flod_ev.duration = timedelta(seconds=10)
        cal.events.add(flod_ev)
    for f in fjara:
        fjara_ev = Event()
        fjara_ev.name = "Fjara"
        fjara_ev.dtstamp = datetime.now()
        fjara_ev.description = "%s : %5.2f m" % f 
        fjara_ev.begin = f[0]
        fjara_ev.duration = timedelta(seconds=10)
        cal.events.add(fjara_ev)
    
    with open(args.out, 'w') as f:
        f.writelines(cal)

    # for idx, date in enumerate(dates):
        # print("%s %9.3f %9.3f %9.3f %9.3f %9.3f %9.3f %9.3f" %
        #       (date, lats[idx], lons[idx], tide[idx], lp[idx], tide[idx] +
        #        lp[idx], tide[idx] + lp[idx] + load[idx], load[idx]))

if __name__ == '__main__':
    main()
