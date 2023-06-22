import calendar
import logging
import pprint
import time
from collections import defaultdict
from datetime import datetime
from geopy.distance import geodesic as gd
import requests
import pandas as pd


class FlightInfo(object):
    __slots__ = ["DepartureAirport_ICAO", "ArrivalAirport_ICAO",
                 "DepartureTime", "ArrivalTime", "DISTANCE",
                 "DepartureAirport_IATA", "ArrivalAirport_IATA", "Callsign"]

    def __init__(self, DepartureAirport_ICAO=None, ArrivalAirport_ICAO=None,
                 DepartureTime=None, ArrivalTime=None, DISTANCE=None, DepartureAirport_IATA=None,
                 ArrivalAirport_IATA=None, Callsign=None):
        self.DepartureAirport_ICAO = DepartureAirport_ICAO
        self.ArrivalAirport_ICAO = ArrivalAirport_ICAO
        self.DepartureTime = DepartureTime
        self.ArrivalTime = ArrivalTime
        self.DISTANCE = DISTANCE
        self.DepartureAirport_IATA = DepartureAirport_IATA
        self.ArrivalAirport_IATA = ArrivalAirport_IATA
        self.Callsign = Callsign

    def __repr__(self):
        attrib_value = {"DepartureAirport_ICAO": self.DepartureAirport_ICAO,
                        "ArrivalAirport_ICAO": self.ArrivalAirport_ICAO,
                        "DepartureTime": self.DepartureTime,
                        "ArrivalTime": self.ArrivalTime,
                        "DISTANCE": self.DISTANCE,
                        "DepartureAirport_IATA": self.DepartureAirport_IATA,
                        "ArrivalAirport_IATA": self.ArrivalAirport_IATA,
                        "Callsign": self.Callsign}
        return str(attrib_value)

    def __dict__(self):
        attrib_value = {"DepartureAirport_ICAO": [self.DepartureAirport_ICAO],
                        "ArrivalAirport_ICAO": [self.ArrivalAirport_ICAO],
                        "DepartureTime": [self.DepartureTime],
                        "ArrivalTime": [self.ArrivalTime],
                        "DISTANCE": [self.DISTANCE],
                        "DepartureAirport_IATA": [self.DepartureAirport_IATA],
                        "ArrivalAirport_IATA": [self.ArrivalAirport_IATA],
                        "Callsign": [self.Callsign]}
        return attrib_value

    def __str__(self):
        attrib_value = {"DepartureAirport_ICAO": self.DepartureAirport_ICAO,
                        "ArrivalAirport_ICAO": self.ArrivalAirport_ICAO,
                        "DepartureTime": self.DepartureTime,
                        "ArrivalTime": self.ArrivalTime,
                        "DISTANCE": self.DISTANCE,
                        "DepartureAirport_IATA": self.DepartureAirport_IATA,
                        "ArrivalAirport_IATA": self.ArrivalAirport_IATA,
                        "Callsign": self.Callsign}
        return str(attrib_value)

    def to_pandas_df(self):
        return pd.DataFrame(self.__dict__())


class OpenSkyApi(object):
    __slots__ = ['_auth', '__sess', '__base_url', '_airports']

    def __init__(self, login=None, password=None):
        self._auth = (login, password)
        self.__sess = requests.Session()
        self.__base_url: str = 'https://opensky-network.org/api'
        self._airports = pd.read_csv('world_airports.csv')

    def __get_flights_json(self, operation, params):
        r = self.__sess.get(
            f"{self.__base_url}{operation}",
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
        flights = []
        if flights_json is not None:
            for flight in flights_json:
                fl = FlightInfo(DepartureAirport_ICAO=flight['estDepartureAirport'],
                                ArrivalAirport_ICAO=flight['estArrivalAirport'],
                                DepartureTime=flight['firstSeen'],
                                ArrivalTime=flight['lastSeen'],
                                Callsign=flight['Callsign']
                                )
                flights.append(fl)
            return fl
        return None

    # def parse_flyghts(self):
    #     flight =
