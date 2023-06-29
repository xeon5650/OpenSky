import OpenSky

api = OpenSky.OpenSkyApi('Zabolotskikh','TT7.622023.')
p = api.get_departures_by_airport('KPSP','2023-06-15T00:00:00Z','2023-06-22T00:00:00Z',False)

p.to_pandas_df().to_csv('TEST.csv')
print(p.to_dict())

