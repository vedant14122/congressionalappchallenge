import math
from decimal import Decimal
from typing import Tuple


def calculate_distance(lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    # Convert to radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    r = 6371
    
    return c * r


def get_neighborhood(lat: Decimal, lon: Decimal) -> str:
    """
    Determine LA neighborhood based on coordinates
    This is a simplified version - in production you'd use a proper geocoding service
    """
    lat_f = float(lat)
    lon_f = float(lon)
    
    # Simplified LA neighborhood boundaries
    # In production, use proper GIS data or geocoding service
    
    # Downtown LA / Skid Row
    if (34.04 <= lat_f <= 34.06 and -118.26 <= lon_f <= -118.24):
        return "Skid Row"
    
    # Koreatown
    if (34.05 <= lat_f <= 34.08 and -118.32 <= lon_f <= -118.28):
        return "Koreatown"
    
    # Hollywood
    if (34.08 <= lat_f <= 34.12 and -118.36 <= lon_f <= -118.32):
        return "Hollywood"
    
    # Venice
    if (33.98 <= lat_f <= 34.02 and -118.48 <= lon_f <= -118.44):
        return "Venice"
    
    # South LA
    if (33.95 <= lat_f <= 34.05 and -118.32 <= lon_f <= -118.24):
        return "South LA"
    
    # San Fernando Valley
    if (34.15 <= lat_f <= 34.25 and -118.50 <= lon_f <= -118.35):
        return "San Fernando Valley"
    
    # San Pedro / Harbor
    if (33.70 <= lat_f <= 33.80 and -118.32 <= lon_f <= -118.28):
        return "San Pedro/Harbor"
    
    # Westlake / MacArthur Park
    if (34.06 <= lat_f <= 34.08 and -118.28 <= lon_f <= -118.26):
        return "Westlake/MacArthur Park"
    
    return "Other"


def is_within_radius(lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal, radius_km: float) -> bool:
    """
    Check if two points are within specified radius
    """
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    return distance <= radius_km


def format_distance(distance_km: float) -> str:
    """
    Format distance for display
    """
    if distance_km < 1:
        return f"{int(distance_km * 1000)}m"
    elif distance_km < 10:
        return f"{distance_km:.1f}km"
    else:
        return f"{int(distance_km)}km"
