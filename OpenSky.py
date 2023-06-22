import calendar
import logging
import pprint
import time
from collections import defaultdict
from datetime import datetime
from geopy.distance import geodesic as gd
import requests
import pandas as pd


class Flight(object):
    keys = [
        "icao24",
        "firstSeen",
        "estDepartureAirport",
        "lastSeen",
        "estArrivalAirport",
        "callsign",
        "estDepartureAirportHorizDistance",
        "estDepartureAirportVertDistance",
        "estArrivalAirportHorizDistance",
        "estArrivalAirportVertDistance",
        "departureAirportCandidatesCount",
        "arrivalAirportCandidatesCount",
    ]

    def __init__(self, arr):
        self.__dict__ = dict(zip(Flight.keys, arr))

    def __repr__(self):
        return f"{repr(self.__dict__)}"

    def __str__(self):
        return pprint.pformat(self.__dict__, indent=4)


class OpenSkyApi(object):
    __slots__ = ['_auth', '__sess', '__base_url', '_airports']

    def __init__(self, login=None, password=None):
        self._auth = (login, password)
        self.__sess = requests.Session()
        self.__base_url: str = 'https://opensky-network.org/api'
        self._airports = pd.read_csv('world_airports.csv')

    def __get_flights_json(self, operation, params):
        r = requests.get(
            "{0:s}{1:s}".format(self.__base_url, operation),
            auth=self._auth,
            params=params,
            timeout=30,
        )
        if r.status_code == 200:
            return r.json()

        else:
            logging.error(
                f"Request for {params} "
                f"Error occurred: {r.status_code}"
            )
        return None

    def get_arrivals_by_airport(self, airport, start, end):

        params = {"airport": airport, "begin": start, "end": end}
        flights_json = self.__get_flights_json(
            "/flights/arrival", params=params
        )

        if flights_json is not None:
            return [Flight(list(entry.values())) for entry in flights_json]
        return None

    def __calc_distanse(self, dep_icao, arr_icao):
        coordinates = self._airports
        try:
            from_lat = coordinates[coordinates['ICAO'] == dep_icao]['Latitude'].tolist()[0]
            from_lon = coordinates[coordinates['ICAO'] == dep_icao]['Longitude'].tolist()[0]
            to_lat = coordinates[coordinates['ICAO'] == arr_icao]['Latitude'].tolist()[0]
            to_lon = coordinates[coordinates['ICAO'] == arr_icao]['Longitude'].tolist()[0]

            distance = gd((round(float(from_lat), 3), round(float(from_lon), 3)),
                          (round(float(to_lat), 3), round(float(to_lon), 3))).km
            distance = round(float(distance), 3)
            return distance
        except Exception as e:
            print(e)

    def get_departures_by_airport(self, airport, begin, end):

        if begin >= end:
            raise ValueError("The end daytame must be greater than begin.")
        if end - begin > 604800:
            raise ValueError("The time interval must be smaller than 7 days.")

        params = {"airport": airport, "begin": begin, "end": end}
        flights_json = self.__get_flights_json(operation="/flights/departure", params=params)

        if flights_json is not None:
            return [Flight(list(entry.values())) for entry in flights_json]
        return None

    # def parse_flyghts(self):
    #     flight =


