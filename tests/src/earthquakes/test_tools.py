import pytest 
from earthquakes.tools import get_haversine_distance
import numpy as np

@pytest.mark.parametrize("earthquake_latitudes, earthquake_longitudes, asset_latitude, asset_longitude, expected",
                         [[0, 0, 0, 0, 0],
                         [1, 1, 0, 0, 157.2],
                         [0, 0, 1, 1, 157.2],
                         [35.025, 25.763, 35.169, 26.215, 44.15],
                         [35.025, 25.763, 35.631, 27.153, 143]])

#References from https://www.movable-type.co.uk/scripts/latlong.html


def test_get_haversine_distance(earthquake_latitudes, 
                                earthquake_longitudes, 
                                asset_latitude, 
                                asset_longitude,
                                expected
                               ):
    
    test = get_haversine_distance(earthquake_latitudes, 
                                  earthquake_longitudes, 
                                  asset_latitude, 
                                  asset_longitude
                                 )
                          
    np.testing.assert_allclose(test, expected, atol=1) #Comparaison to the kilometer
        