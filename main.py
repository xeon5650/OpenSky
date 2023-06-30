import open_sky

api = open_sky.OpenSkyApi('Zabolotskikh', 'TT7.622023.')
p = api.get_departures_by_airport('EHAM', '2023-06-11T00:00:00Z', '2023-06-15T00:00:00Z')

p.to_pandas_df().to_csv('departure.csv')

p = api.get_arrivals_by_airport('EHAM', '2023-06-11T00:00:00Z', '2023-06-15T00:00:00Z')

p.to_pandas_df().to_csv('arrivals.csv')
