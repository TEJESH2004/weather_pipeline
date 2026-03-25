import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = [
    {"name": "Hyderabad", "lat": 17.38, "lon": 78.49},
    {"name": "Mumbai",    "lat": 19.07, "lon": 72.87},
    {"name": "Delhi",     "lat": 28.61, "lon": 77.20},
]

def extract_weather(city: dict) -> dict:
    """
    Hits Open-Meteo API for a given city.
    Returns raw JSON exactly as the API sent it.
    Does NOT transform or clean anything.
    """
    params = {
        "latitude":  city["lat"],
        "longitude": city["lon"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "past_days": 30,
        "timezone":  "auto"
    }

    response = requests.get(BASE_URL, params=params)

    # crash immediately if API returns an error
    response.raise_for_status()

    data = response.json()

    # validate the shape — fail loudly if API changed
    assert "daily" in data,                        "Missing 'daily' key in response"
    assert "time" in data["daily"],                "Missing 'time' in daily data"
    assert "temperature_2m_max" in data["daily"],  "Missing temperature data"
    assert len(data["daily"]["time"]) > 0,         "API returned zero records"

    # tag with city name — not in API response
    data["city"] = city["name"]

    print(f"Extracted {len(data['daily']['time'])} days for {city['name']}")

    return data


if __name__ == "__main__":
    for city in CITIES:
        raw = extract_weather(city)
        print(f"  First date:  {raw['daily']['time'][0]}")
        print(f"  Last date:   {raw['daily']['time'][-1]}")
        print(f"  Sample temp: {raw['daily']['temperature_2m_max'][0]}°C")
        print()