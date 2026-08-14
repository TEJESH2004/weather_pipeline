from extractor   import extract_weather
from transformer import transform_weather
from loader      import load_weather

CITIES = [
    {"name": "Hyderabad", "lat": 17.38, "lon": 78.49},
    {"name": "Mumbai",    "lat": 19.07, "lon": 72.87},
    {"name": "Delhi",     "lat": 28.61, "lon": 77.20},
]

def run_pipeline():
    for city in CITIES:
        print(f"\nProcessing {city['name']}...")
        raw = extract_weather(city)
        df  = transform_weather(raw)
        load_weather(df)
    print("\nPipeline complete.")

if __name__ == "__main__":
    run_pipeline()