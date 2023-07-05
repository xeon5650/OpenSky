import open_sky

"""Create api object and login in to OpenSky"""
api = open_sky.OpenSkyApi('login', 'password')

"""Get departing flights from airport"""
departures = api.get_departures_by_airport('KPSP', '2023-06-11T00:00:00Z', '2023-06-15T00:00:00Z')
"""Convert to pandas df and save in csv"""
departures.to_pandas_df().to_csv('departure.csv', index=False)

"""Get arrivals flights from airport"""
arrivals = api.get_arrivals_by_airport('KPSP', '2023-06-11T00:00:00Z', '2023-06-15T00:00:00Z')
"""Convert to pandas df and save in csv"""
arrivals.to_pandas_df().to_csv('arrivals.csv', index=False)

all_flights = departures.extend(arrivals)
all_flights.to_pandas_df().to_csv('all.csv', index=False)
