import pandas as pd

def transform_weather(raw: dict) ->pd.DataFrame:
	daily = raw["daily"]

	df = pd.DataFrame({
	"date":	daily["time"],
	"temp_max":	daily["temperature_2m_max"],
	"temp_min": daily["temperature_2m_min"],
	"precipitation":	daily["precipitation_sum"],
	"wind_speed":	daily["wind_speed_10m_max"],
	})

	df["date"]=pd.to_datetime(df["date"]).dt.date
	df=df.dropna(subset=["temp_max"])

	df["city"]=raw["city"]

	df=df[["city","date","temp_max","temp_min","precipitation","wind_speed"]]

	print(f"Transformed {len(df)} rows for {raw['city']}")

	return df

if __name__ == "__main__":
	from extractor import extract_weather
	
	city = {"name":"Hyderabad", "lat":17.38, "lon" :78.48}
	raw =extract_weather(city)
	df= transform_weather(raw)
	
	print(df.head())
	print(df.dtypes)