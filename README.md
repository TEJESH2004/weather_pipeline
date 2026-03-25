\# Weather Pipeline



An ETL pipeline that pulls weather data from the Open-Meteo API,

cleans it with pandas, and loads it into PostgreSQL.

Orchestrated with Apache Airflow.



\## Tech stack

\- Python, pandas

\- PostgreSQL

\- Apache Airflow

\- AWS S3 + Glue (adding in Week 2)



\## Pipeline flow

Open-Metro API → extractor.py → transformer.py → loader.py → PostgreSQL



\## How to run locally

1\. Create and activate virtual environment

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate



2\. Install dependencies

&#x20;  pip install -r requirements.txt



3\. Run the pipeline

&#x20;  python src/extractor.py



