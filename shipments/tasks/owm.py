from django.core.cache import cache
from shipments.models import Address, Location
from shipments.utils.openweathermap import geocoding_to_coordinates, coordinates_to_weather
from django.conf import settings
import time

# Constants
OWM_HOURLY_LIMIT = settings.OWM_HOURLY_LIMIT
OWM_CACHE_TIMEOUT = settings.OWM_CACHE_TIMEOUT
TIMEOUT = 408
TOO_MANY_REQUESTS = 429
UNAUTHORIZED = 401
NOT_FOUND = 404
COUNTER_KEY = "owm_request_counter"
TIMESTAMP_KEY = "owm_timestamp_start"

cache.set(COUNTER_KEY, 0)

def handle_rate_limiting():
    current_counter = cache.get(COUNTER_KEY, 0)
    timestamp_start = cache.get(TIMESTAMP_KEY, time.time())
    now = time.time()
    if now - timestamp_start > 3600:  
        current_counter = 0
        cache.set(TIMESTAMP_KEY, now)

    if current_counter >= OWM_HOURLY_LIMIT:
        return False
    return True

def handle_api_response(status):
    if status != TIMEOUT:
        cache.incr(COUNTER_KEY)
    if status in [TOO_MANY_REQUESTS, UNAUTHORIZED]:  
        cache.set(COUNTER_KEY, OWM_HOURLY_LIMIT)

def get_location_from_address(address):
    if address.location:
        return address.location.lat, address.location.lon
    lat, lon, status = geocoding_to_coordinates(address.zipcode, address.country.code)
    handle_api_response(status)
    if status == NOT_FOUND:
        return None, None
    if lat and lon:
        address.location = Location.objects.create(lat=lat, lon=lon)
        address.save()
        return lat, lon
    return None, None

def geocoding_to_weather_cache(address_id: int) -> dict:
    address = Address.objects.get(pk=address_id)
    weather_cache_key = f"weather_{address.zipcode}_{address.country.code}"
    cached_weather = cache.get(weather_cache_key)
    
    if cached_weather:
        return cached_weather
    if not handle_rate_limiting():
        return None

    lat, lon = get_location_from_address(address)
    if not lat or not lon:
        cache.set(weather_cache_key, None, timeout=OWM_CACHE_TIMEOUT)
        return None

    weather, status = coordinates_to_weather(lat, lon)
    handle_api_response(status)

    if weather:
        cache.set(weather_cache_key, weather, timeout=OWM_CACHE_TIMEOUT)
    return weather
