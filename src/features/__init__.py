import numpy as np

def distance(lat1, lon1, lat2, lon2):
    """Calculate distance in miles between two coordinates"""
    # approximate radius of earth in miles
    R = 3959

    lat1 = lat1 * np.pi / 180.0
    lon1 = np.deg2rad(lon1)
    lat2 = np.deg2rad(lat2)
    lon2 = np.deg2rad(lon2)

    d = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2

    return 2 * R * np.arcsin(np.sqrt(d))