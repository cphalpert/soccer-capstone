import pandas as pd
import pickle

years = range(2008, 2018)

arrivals = pd.DataFrame()
departures = pd.DataFrame()

for year in years:
    df = pickle.load( open( "year-{}.p".format(year), "rb" ) )
    
    new_arrivals = pd.concat(df[::2])
    new_departures = pd.concat(df[1::2])

    arrivals = pd.concat([arrivals, new_arrivals])
    departures = pd.concat([departures, new_departures])


arrivals = arrivals.reset_index()
departures = departures.reset_index()

arrivals.to_pickle('arrivals.p')
departures.to_pickle('departures.p')
