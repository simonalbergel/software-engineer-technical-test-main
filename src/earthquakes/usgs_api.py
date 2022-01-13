from urllib.parse import urlencode
import pandas as pd
import aiohttp
import asyncio
import io

API_URL_QUERY = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'

def build_api_url(
    latitude,
    longitude,
    radius, 
    minimum_magnitude,
    end_date,
    start_date,
    data_format='csv',
) -> str:
    
    parameters = {'format' : data_format, 
                  'starttime' : start_date,
                  'endtime' : end_date,
                  'minmagnitude' : minimum_magnitude,
                  'maxradiuskm' : radius, 
                  'latitude' : latitude,
                  'longitude' : longitude}
    
    query = urlencode(parameters)
    
    return API_URL_QUERY + query
    
def get_earthquake_data(
    latitude, 
    longitude, 
    radius, 
    minimum_magnitude, 
    end_date, 
    start_date,
) -> pd.DataFrame:
    
    api_url = build_api_url(latitude,
                            longitude,
                            radius, 
                            minimum_magnitude,
                            '{:%Y-%m-%d}'.format(end_date),
                            '{:%Y-%m-%d}'.format(start_date),
                           )
    df = pd.read_csv(api_url)
    
    return df

async def get_earthquake_data_for_single_locations(session, api_url):
    async with session.get(api_url) as request:
        earthquake_data = await request.text()
        df = pd.read_csv(io.StringIO(earthquake_data), sep=',')
        return df

async def get_earthquake_data_for_multiple_locations(assets, radius, minimum_magnitude, end_date, start_date):
    async with aiohttp.ClientSession() as session: 
        
        tasks = []
        for asset in assets:
            api_url = build_api_url(asset[0],
                                    asset[1],
                                    radius, 
                                    minimum_magnitude,
                                    end_date,
                                    start_date)
            tasks.append(asyncio.ensure_future(get_earthquake_data_for_single_locations(session, api_url)))
            
        dfs = await asyncio.gather(*tasks)
        df = pd.concat(dfs, axis=0)
        
        return df
            
                