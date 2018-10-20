import numpy as np

## Input: 2 GPS coordinates in degrees
## Output: distance between the two points in meters.
def gps_distance(lon1, lat1, lon2, lat2):
    R = 6371e3
    phi1 = np.deg2rad(lat1)
    phi2 = np.deg2rad(lat2)
    delta_phi = np.deg2rad(lat2 - lat1)
    delta_lambda = np.deg2rad(lon2 - lon1)

    a = np.sin(delta_phi/2) * np.sin(delta_phi/2) + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2) * np.sin(delta_lambda/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c / 1000.0
