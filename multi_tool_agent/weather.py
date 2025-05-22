import requests
from typing import Optional, List, Dict
import os

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "your-default-api-key")

def get_extended_weather_forecast(lat: float, lon: float) -> Optional[List[Dict[str, str]]]:
    """
    Fetch the extended weather forecast from the U.S. National Weather Service (NWS) API
    based on a given latitude and longitude.

    Args:
        lat (float): Latitude of the location (e.g., 38.8977).
        lon (float): Longitude of the location (e.g., -77.0365).

    Returns:
        Optional[List[Dict[str, str]]]: A list of forecast dictionaries for each time period,
        each containing:
            - 'name': Name of the forecast period (e.g., "Today", "Tonight")
            - 'startTime': ISO timestamp for the start of the forecast period
            - 'temperature': Temperature value
            - 'temperatureUnit': Temperature unit (e.g., "F" or "C")
            - 'windSpeed': Wind speed description
            - 'windDirection': Wind direction (e.g., "NW")
            - 'shortForecast': Short summary (e.g., "Partly Sunny")
            - 'detailedForecast': Full text forecast

        Returns None if data is unavailable or an error occurs.
    """
    headers = {
        'User-Agent': 'MyWeatherApp (doug@roitraining.com)',  # Replace with your actual email
        'Accept': 'application/geo+json'
    }

    # Step 1: Get metadata to find forecast URL
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(points_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching data from points endpoint: {response.status_code}")
        return None

    points_data = response.json()
    forecast_url = points_data['properties'].get('forecast')
    if not forecast_url:
        print("Forecast URL not found in response.")
        return None

    # Step 2: Fetch the forecast data
    forecast_response = requests.get(forecast_url, headers=headers)
    if forecast_response.status_code != 200:
        print(f"Error fetching forecast: {forecast_response.status_code}")
        return None

    forecast_data = forecast_response.json()
    periods = forecast_data['properties'].get('periods', [])

    if not periods:
        print("No forecast periods found in response.")
        return None

    # Return the full extended forecast
    extended_forecast = []
    for period in periods:
        extended_forecast.append({
            'name': period['name'],
            'startTime': period['startTime'],
            'temperature': str(period['temperature']),
            'temperatureUnit': period['temperatureUnit'],
            'windSpeed': period['windSpeed'],
            'windDirection': period['windDirection'],
            'shortForecast': period['shortForecast'],
            'detailedForecast': period['detailedForecast']
        })

    return extended_forecast


def get_lat_lon(city: str, state: str) -> Optional[Dict[str, float]]:
    """
    Use the Google Maps Geocoding API to convert city and state to latitude and longitude.

    Args:
        city (str): City name
        state (str): State abbreviation or full name
        api_key (str): Google Maps API key

    Returns:
        Optional[Dict[str, float]]: {'lat': ..., 'lon': ...} or None on failure
    """
    address = f"{city}, {state}"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Geocoding API error: {response.status_code}")
        return None

    data = response.json()
    if not data['results']:
        print("No results found for the given location.")
        return None

    location = data['results'][0]['geometry']['location']
    return {'lat': location['lat'], 'lon': location['lng']}

