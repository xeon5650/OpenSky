import OpenSky


# api = OpenSky.OpenSkyApi('Zabolotskikh','TT7.622023.')
# p = api.get_arrivals_by_airport('KPSP',1687132800,1687219200)
# for flight in p:
#     flight = OpenSky.Flight(flight)
#     print(flight)
#
# print(p)
#
fl = OpenSky.FlightInfo(1,1,1,1,1,1,1,1)
print(fl.__dict__())
