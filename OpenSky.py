import logging
import datetime
from datetime import datetime
from geopy.distance import geodesic as gd
import requests
import pandas as pd


class FlightData:
    def __get_iata_by_icao(self, icao):
        coordinates = self._airports
        try:
            iata = coordinates[coordinates['ICAO'] == icao]['IATA'].tolist()[0]
            return iata
        except Exception as e:
            print("IATA not found")
            return None

    def __unix_to_iso(self, unix_time):
        iso_time = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%SZ')

        return iso_time

    def __calc_distance(self, dep_icao, arr_icao):
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
            print("Airports coordinates not found")
            return None

    def __init__(self, flights_json):
        self._airports = pd.read_csv('world_airports.csv', names=['Airport ID',
                                                                  'Name',
                                                                  'City',
                                                                  'Country',
                                                                  'IATA',
                                                                  'ICAO',
                                                                  'Latitude',
                                                                  'Longitude',
                                                                  'Altitude',
                                                                  'Timezone',
                                                                  'DST',
                                                                  'Tz database time zone',
                                                                  'Type',
                                                                  'Source'
                                                                  ])
        self._flights = [None] * len(flights_json)
        for flight in enumerate(flights_json, start=0):
            flights_data = FlightData.FlightObject()
            dep_icao = flight[1]['estDepartureAirport']
            arr_icao = flight[1]['estArrivalAirport']
            distance = self.__calc_distance(dep_icao, arr_icao)
            flights_data.DepartureAirport_ICAO = dep_icao
            flights_data.ArrivalAirport_ICAO = arr_icao
            flights_data.DepartureTime = self.__unix_to_iso(flight[1]['firstSeen'])
            flights_data.ArrivalTime = self.__unix_to_iso(flight[1]['lastSeen'])
            flights_data.DISTANCE = distance
            flights_data.DepartureAirport_IATA = self.__get_iata_by_icao(dep_icao)
            flights_data.ArrivalAirport_IATA = self.__get_iata_by_icao(arr_icao)
            flights_data.Callsign = flight[1]['callsign']
            self[flight[0]] = flights_data

    def __len__(self):
        return len(self._flights)

    def __setitem__(self, flight_number, flight_object):
        self._flights[flight_number] = flight_object

    def __getitem__(self, flight_number):
        return self._flights[flight_number]

    def to_dict(self):

        dict = {'DepartureAirport_ICAO': [entry.DepartureAirport_ICAO for entry in self],
                'ArrivalAirport_ICAO': [entry.ArrivalAirport_ICAO for entry in self],
                'DepartureTime': [entry.DepartureTime for entry in self],
                'ArrivalTime': [entry.ArrivalTime for entry in self],
                'DISTANCE': [entry.DISTANCE for entry in self],
                'DepartureAirport_IATA': [entry.DepartureAirport_IATA for entry in self],
                'ArrivalAirport_IATA': [entry.ArrivalAirport_IATA for entry in self],
                'Callsign': [entry.Callsign for entry in self],
                }
        return dict

    def to_pandas_df(self):
        return pd.DataFrame(self.to_dict())

    class FlightObject:
        __slots__ = ["DepartureAirport_ICAO", "ArrivalAirport_ICAO",
                     "DepartureTime", "ArrivalTime",
                     "DISTANCE", "DepartureAirport_IATA",
                     "ArrivalAirport_IATA", "Callsign"]

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
            attrib_value = {f"DepartureAirport_ICAO - {self.DepartureAirport_ICAO}",
                            f"ArrivalAirport_ICAO - {self.ArrivalAirport_ICAO}",
                            f"DepartureTime - {self.DepartureTime}",
                            f"ArrivalTime - {self.ArrivalTime}",
                            f"DISTANCE - {self.DISTANCE}",
                            f"DepartureAirport_IATA - {self.DepartureAirport_IATA}",
                            f"ArrivalAirport_IATA - {self.ArrivalAirport_IATA}",
                            f"Callsign {self.Callsign}"}
            return str(attrib_value)

        def to_pandas_df(self):
            return pd.DataFrame(self.__dict__())


class OpenSkyApi(object):
    __slots__ = ['_auth', '__sess', '__base_url', '_airports']


    def __iso_to_unix(self,date_iso):
        date_format = datetime.strptime(date_iso,
                                                 "%Y-%m-%dT%H:%M:%SZ")
        unix_time = int(datetime.timestamp(date_format))
        return unix_time

    def __init__(self, login=None, password=None):
        self._auth = (login, password)
        self.__sess = requests.Session()
        self.__base_url: str = 'https://opensky-network.org/api'
        self._airports = pd.read_csv('world_airports.csv', names=['Airport ID',
                                                                  'Name',
                                                                  'City',
                                                                  'Country',
                                                                  'IATA',
                                                                  'ICAO',
                                                                  'Latitude',
                                                                  'Longitude',
                                                                  'Altitude',
                                                                  'Timezone',
                                                                  'DST',
                                                                  'Tz database time zone',
                                                                  'Type',
                                                                  'Source'
                                                                  ])

    def __get_flights_json(self, operation, params):
        r = self.__sess.get(
            f"{self.__base_url}{operation}",
            auth=self._auth,
            params=params
        )
        if r.status_code == 200:
            return r.json()

        else:
            logging.error(
                f"Request for {params} "
                f"Error occurred: {r.status_code}"
            )
        return None

    def get_arrivals_by_airport(self, airport, start, end, json_output=True):
        start = self.__iso_to_unix(start)
        print(start)
        end = self.__iso_to_unix(end)
        if start >= end:
            raise ValueError("The end daytame must be greater than start.")
        if end - start > 604800:
            raise ValueError("The time interval must be smaller than 7 days.")

        params = {"airport": airport, "begin": start, "end": end}
        flights_json = self.__get_flights_json(
            "/flights/arrival", params=params
        )
        flights_obj = FlightData(flights_json)
        if json_output:
            return flights_json
        else:
            return flights_obj

    def get_departures_by_airport(self, airport, start, end, json_output=True):
        start = self.__iso_to_unix(start)
        print(start)
        end = self.__iso_to_unix(end)
        if start >= end:
            raise ValueError("The end daytame must be greater than start.")
        if end - start > 604800:
            raise ValueError("The time interval must be smaller than 7 days.")

        params = {"airport": airport, "begin": start, "end": end}
        flights_json = self.__get_flights_json(
            "/flights/departure", params=params
        )
        flights_obj = FlightData(flights_json)
        if json_output:
            return flights_json
        else:
            return flights_obj
