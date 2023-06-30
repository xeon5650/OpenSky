"""Module for interacting with OpenSky"""
import logging
import datetime
from datetime import datetime
from geopy.distance import geodesic as gd
import requests
import pandas


class FlightData:
    """Class for store flightData"""

    def __get_iata_by_icao(self, icao) -> str | None:
        """
        Search IATA code by ICAO
        :param icao: specified airport ICAO code
        :return: airport IATA code
        """
        coordinates = self._airports
        try:
            iata = coordinates[coordinates['ICAO'] == icao]['IATA'].tolist()[0]
            return iata
        except IndexError:
            print("IATA not found")
            return None

    @staticmethod
    def __unix_to_iso(unix_time) -> str:
        """
        Conver DateTime in unix to time in ISO
        :param unix_time: DateTime in Unix format
        :return: time in ISO format %Y-%m-%dT%H:%M:%SZ
        """

        iso_time = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%SZ')

        return iso_time

    def __calc_distance(self, dep_icao, arr_icao) -> float | None:
        """
        Calc distance between airports by their ICAO codes
        :param dep_icao: Airport icao code
        :param arr_icao: Airport icao code
        :return: distance in Km
        """
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
        except IndexError:
            print("Airports coordinates not found ",dep_icao, arr_icao)
            return None

    __slots__ = ['_airports', '_flights']

    def __init__(self, flights_json):
        """
        Initialize Flight data object
        :param flights_json: json with flight info
        """
        self._airports = pandas.read_csv('world_airports.csv', names=['Airport ID',
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
            flights_data.departure_airport_icao = dep_icao
            flights_data.arrival_airport_icao = arr_icao
            flights_data.departure_time = self.__unix_to_iso(flight[1]['firstSeen'])
            flights_data.arrival_time = self.__unix_to_iso(flight[1]['lastSeen'])
            flights_data.distance = distance
            flights_data.departure_airport_iata = self.__get_iata_by_icao(dep_icao)
            flights_data.arrival_airport_iata = self.__get_iata_by_icao(arr_icao)
            flights_data.call_sign = flight[1]['callsign']
            self[flight[0]] = flights_data

    def __len__(self) -> int:
        """
        :return: number of elements in FlightData
        """
        return len(self._flights)

    def __setitem__(self, flight_number, flight_object):
        """
        set FlightObject in FlightData by specified index
        :param flight_number: specified index
        :param flight_object: FlightObject
        :return: FlightObject
        """
        self._flights[flight_number] = flight_object

    def __getitem__(self, flight_number):
        """
        Return FlightObject with specified index from FlightData
        :param flight_number: specified index
        :return: FlightObject
        """
        return self._flights[flight_number]

    def to_dict(self) -> dict:
        """
        Convert FlightData to dictionary
        :return: dict
        """

        dictionary = {'DepartureAirport_ICAO': [entry.departure_airport_icao for entry in self],
                      'ArrivalAirport_ICAO': [entry.arrival_airport_icao for entry in self],
                      'DepartureTime': [entry.departure_time for entry in self],
                      'ArrivalTime': [entry.arrival_time for entry in self],
                      'DISTANCE': [entry.distance for entry in self],
                      'DepartureAirport_IATA': [entry.departure_airport_iata for entry in self],
                      'ArrivalAirport_IATA': [entry.arrival_airport_iata for entry in self],
                      'Callsign': [entry.call_sign for entry in self],
                      }
        return dictionary

    def to_pandas_df(self) -> pandas.DataFrame:
        """
        Convert FlightData to Pandas DataFrame
        :return: Pandas DataFrame
        """
        return pandas.DataFrame(self.to_dict())

    class FlightObject:
        """Class for store flightData
        Attributes:
            departure_airport_icao - Departure airport code in ICAO
            arrival_airport_icao - Arrival airport code in ICAO
            departure_time - Departure time in ISO format
            arrival_time - Arrival time in ISO format
            distance - Distance between departure and arrival airports
            departure_airport_iata - Departure airport code in IATA
            arrival_airport_iata - Arrival airport code in IATA
            call_sign - Aircraft call sign
        """

        __slots__ = ["departure_airport_icao", "arrival_airport_icao",
                     "departure_time", "arrival_time",
                     "distance", "departure_airport_iata",
                     "arrival_airport_iata", "call_sign"]

        def __init__(self, departure_airport_icao=None, arrival_airport_icao=None,
                     departure_time=None, arrival_time=None, distance=None,
                     departure_airport_iata=None, arrival_airport_iata=None,
                     call_sign=None):
            """
            Initialize FlightObject
            :param departure_airport_icao: Departure airport code in ICAO
            :param arrival_airport_icao: Arrival airport code in ICAO
            :param departure_time: Departure time in ISO format
            :param arrival_time: Arrival time in ISO format
            :param distance: Distance between departure and arrival airports
            :param departure_airport_iata: Departure airport code in IATA
            :param arrival_airport_iata: Arrival airport code in IATA
            :param call_sign: Aircraft call sign
            """
            self.departure_airport_icao = departure_airport_icao
            self.arrival_airport_icao = arrival_airport_icao
            self.departure_time = departure_time
            self.arrival_time = arrival_time
            self.distance = distance
            self.departure_airport_iata = departure_airport_iata
            self.arrival_airport_iata = arrival_airport_iata
            self.call_sign = call_sign

        def __repr__(self):
            """Return printed representation of FlightObject"""
            attrib_value = f"FlightObject(departure_airport_icao = {self.departure_airport_icao}," \
                           f"arrival_airport_icao = {self.arrival_airport_icao}," \
                           f"departure_time = {self.departure_time}," \
                           f"arrival_time= {self.arrival_time}," \
                           f"distance = {self.distance}," \
                           f"departure_airport_iata = {self.departure_airport_iata}" \
                           f"arrival_airport_iata = {self.arrival_airport_iata}," \
                           f"call_sign = {self.call_sign})"
            return str(attrib_value)

        def __str__(self):
            """Return string representation of FlightObject"""
            attrib_value = f"FlightObject(departure_airport_icao = {self.departure_airport_icao}," \
                           f"arrival_airport_icao = {self.arrival_airport_icao}," \
                           f"departure_time = {self.departure_time}," \
                           f"arrival_time= {self.arrival_time}," \
                           f"distance = {self.distance}," \
                           f"departure_airport_iata = {self.departure_airport_iata}" \
                           f"arrival_airport_iata = {self.arrival_airport_iata}," \
                           f"call_sign = {self.call_sign})"
            return str(attrib_value)


class OpenSkyApi:
    """Class for interact with OpenSky api"""
    __slots__ = ['_auth', '__sess', '__base_url', '_airports']

    @staticmethod
    def __iso_to_unix(date_iso) -> int:
        """
        Convert daytime in ISO format to Unix format
        :param date_iso: Daytime in ISO format %Y-%m-%dT%H:%M:%SZ
        :return: Daytime in UNIX format
        """
        date_format = datetime.strptime(date_iso,
                                        "%Y-%m-%dT%H:%M:%SZ")

        unix_time = int(datetime.timestamp(date_format))
        print(unix_time)
        return unix_time

    def __init__(self, login=None, password=None):
        """
        Initialize OpenSkyApi object
        :param login: OpenSky login
        :param password: OpenSky password
        """
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        self._auth = (login, password)
        self.__sess = requests.Session()
        self.__base_url: str = 'https://opensky-network.org/api'
        self._airports = pandas.read_csv('world_airports.csv', names=['Airport ID',
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

    def __get_flights_json(self, operation, params) -> bytes | None:
        """
        Send request to OpenSkyApi and returns Json response
        :param operation: url postfix
        :param params: dictionary of request params
        :return: Json
        """
        response = self.__sess.get(
            f"{self.__base_url}{operation}",
            auth=self._auth,
            params=params
        )
        if response.status_code == 200:
            output = response.json()

        else:
            logging.error(
                "Error occurred:%s", response.status_code
            )
            output = None
        return output

    def get_arrivals_by_airport(self, airport, start, end, json_output=False) -> FlightData | bytes:
        """
        Returns FlightData object or if json_output=True json from OpenSky
         with info about flights arriving at the airport
        The time interval between start and end time must be smaller than 7 days
        :param airport: Airport ICAO code
        :param start: start daytime in ISO
        :param end: end daytime in ISO
        :param json_output: Bool
        :return:FlightData object | json
        """
        start = self.__iso_to_unix(start)
        end = self.__iso_to_unix(end)
        if start >= end:
            raise ValueError("The end daytame must be greater than start.")
        if end - start > 604800:
            raise ValueError("The time interval must be smaller than 7 days.")

        params = {"airport": airport, "begin": start, "end": end}
        flights_json = self.__get_flights_json(
            "/flights/arrival", params=params
        )

        if json_output:
            output = flights_json
        else:
            output = FlightData(flights_json)
        return output

    def get_departures_by_airport(self, airport, start, end, json_output=False) -> FlightData | bytes:
        """
        Returns FlightData object or if json_output=True json from OpenSky
         with info about flights departing from the airport
        The time interval between start and end time must be smaller than 7 days
        :param airport: Airport ICAO code
        :param start: start daytime in ISO
        :param end: end daytime in ISO
        :param json_output: Bool
        :return:FlightData object | json
        """
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

        if json_output:
            output = flights_json
        else:
            output = FlightData(flights_json)
        return output
