import math

def get_distance(lat1, lon1, lat2, lon2):
    """Return distance between two place in kilometers
    Args:
        lat1 (_decimal_): latitude of first point.
        lon1 (_decimal_): longitude of first point.
        lat2 (_decimal_): latitude of second point.
        lon2 (_decimal_): longitude of second point.

    Returns:
        _decimal_: return distance in kilometers
    """    
    R = 6371  # Earth radius in KM

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c # return distance in kilometer.
