import numpy as np
import pandas as pd

EARTH_RADIUS = 6378

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"


def get_haversine_distance(earthquake_latitudes, 
                           earthquake_longitudes, 
                           asset_latitude, 
                           asset_longitude,
)-> pd.DataFrame:
    delta_latitudes_rad = np.radians(asset_latitude - earthquake_latitudes)
    delta_longitudes_rad = np.radians(asset_longitude - earthquake_longitudes)
    earthquake_latitudes_rad = np.radians(earthquake_latitudes)
    asset_latitude_rad = np.radians(asset_latitude)
    
    A = np.power(np.sin((delta_latitudes_rad) / 2), 2)
    B = np.cos(earthquake_latitudes_rad) * np.cos(asset_latitude_rad) * np.power(np.sin((delta_longitudes_rad) / 2), 2)
    
    distances = 2 * EARTH_RADIUS * np.arcsin(np.sqrt(A + B))
    
    return distances

def payout_finder(distance, mag, payout_structure):
    for distance_condition in payout_structure.keys():
        
        if distance <= distance_condition: 
            for mag_condition in payout_structure[distance_condition].keys(): 
                
                if mag >= mag_condition: 
                    return payout_structure[distance_condition][mag_condition]
    return 0

def compute_payouts(earthquake_data, 
                    payout_structure,
                   ):
    
    df = earthquake_data.loc[:,['time', 'mag', 'distance']]
    
    df.loc[:,'datetime'] = pd.to_datetime(df['time'])
    df.set_index(['datetime'], inplace=True)
    df.loc[:,'mag_dist'] = df.loc[:,['mag', 'distance']].to_dict(orient='records')
 
    #There probably is a better way to do this ...
    df_grouped = df.groupby(pd.Grouper(freq='Y'))['mag_dist'].agg([('worstEarthQuake', lambda x: max(x, key = lambda y : payout_finder(y['distance'], y['mag'], payout_structure), default={'mag':0, 'distance':0}))])
    df_grouped.loc[:,'payout'] = df_grouped.loc[:,'worstEarthQuake'].apply(lambda x : payout_finder(x['distance'], x['mag'], payout_structure))
       
    return df_grouped['payout']


def compute_burning_cost(payouts, start_year=1952, end_year=2021):
    
    burning_cost = payouts.loc[str(start_year) + '-01-01' : str(end_year) + '-12-31'].mean()
    
    return burning_cost
    