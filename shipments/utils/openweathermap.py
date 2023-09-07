from django.conf import settings
import requests

OWM_API_KEY = settings.OWM_API_KEY


def geocoding_to_coordinates(zip_code: str, country_code: str) -> tuple:
    """Converts a zip code and country code to coordinates."""
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={OWM_API_KEY}"
    try:
        print(url)
        response = requests.get(url, timeout=2)
    except requests.exceptions.Timeout:
        return None, None, 408
    
    if response.status_code == 200:
        response_json = response.json()
        return response_json['lat'], response_json['lon'], 200
    else:
        return None, None, response.status_code


def coordinates_to_weather(lat: float, lon: float) -> dict:
    """Converts coordinates to weather description."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}"

    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.Timeout:
        return None
    if response.status_code == 200:
        response_json = response.json()
        return response_json['weather'], 200
    else:
        return None, response.status_code