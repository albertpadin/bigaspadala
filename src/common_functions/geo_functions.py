#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import radians, cos, sin, asin, sqrt


def get_distance_in_km(latlon1, latlon2):
    """
        Converts latlong to a distance in KM.
    """
    latlon1 = latlon1.strip().split(',')
    latlon2 = latlon2.strip().split(',')
    try:
        lon1 = float(latlon1[1].strip())
        lat1 = float(latlon1[0].strip())
        lon2 = float(latlon2[1].strip())
        lat2 = float(latlon2[0].strip())
    except:
        return -1
    return haversine(lon1, lat1, lon2, lat2)


def get_distance_in_meters(latlon1, latlon2):
    """
        Converts latlong to a distance in METERS.
    """
    return get_distance_in_km(latlon1, latlon2) * 1000


def haversine(lon1, lat1, lon2, lat2):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def convert_to_lat_lon(latlng):
    latlng = latlng.split(',')
    return latlng[0].strip(), latlng[1].strip()
