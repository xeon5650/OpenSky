import OpenSky

#
# api = OpenSky.OpenSkyApi('Zabolotskikh','TT7.622023.')
# p = api.get_arrivals_by_airport('KPSP',1687132800,1687219200)
# for flight in p:
#     flight = OpenSky.Flight(flight)
#     print(flight)
#
# print(p)

fl = OpenSky.Flights.FlightsData(1,1,1,1,1,1,1,1)
fl2 = OpenSky.Flights.FlightsData(1,1,1,1,1,1,1,1)
fls = OpenSky.Flights([fl,fl2])

for flight in fls:
    print(flight)
