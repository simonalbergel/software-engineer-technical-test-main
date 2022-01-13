import pytest
from datetime import datetime
from earthquakes.usgs_api import build_api_url

@pytest.mark.parametrize("latitude, longitude, radius, minimum_magnitude, end_date, start_date, expected",
                         [[35.025, 25.763, 200, 4.5, datetime(year=2021, month=10, day=21), datetime(year=1821, month=10, day=21), 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=1821-10-21&endtime=2021-10-21&minmagnitude=4.5&maxradiuskm=200&latitude=35.025&longitude=25.763']])

def test_build_api_url(
    latitude,
    longitude,
    radius, 
    minimum_magnitude,
    end_date,
    start_date,
    expected,
    data_format='csv',
):
    test = build_api_url(latitude, 
                         longitude, 
                         radius, 
                         minimum_magnitude, 
                         '{:%Y-%m-%d}'.format(end_date), 
                         '{:%Y-%m-%d}'.format(start_date), 
                         data_format)
    
    assert test == expected
