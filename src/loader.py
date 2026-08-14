import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

DB_CONFIG = {
    "host":     "localhost",
    "database": "weather_pipeline",
    "user":     "postgres",
    "password": "postgres123",
    "port":     5432
}

def load_weather(df: pd.DataFrame) -> None:
    """
    Takes a clean DataFrame from the transformer.
    Upserts rows into the weather_daily Postgres table.
    """
    conn   = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    rows = [
        (
            row["city"],
            row["date"],
            row["temp_max"],
            row["temp_min"],
            row["precipitation"],
            row["wind_speed"],
        )
        for row in df.to_dict("records")
    ]

    sql = """
        INSERT INTO weather_daily (city, date, temp_max, temp_min, precipitation, wind_speed)
        VALUES %s
        ON CONFLICT (city, date)
        DO UPDATE SET
            temp_max      = EXCLUDED.temp_max,
            temp_min      = EXCLUDED.temp_min,
            precipitation = EXCLUDED.precipitation,
            wind_speed    = EXCLUDED.wind_speed
    """

    execute_values(cursor, sql, rows)
    conn.commit()

    print(f"Loaded {len(rows)} rows into weather_daily")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    from extractor   import extract_weather
    from transformer import transform_weather

    city = {"name": "Hyderabad", "lat": 17.38, "lon": 78.49}
    raw  = extract_weather(city)
    df   = transform_weather(raw)
    load_weather(df)