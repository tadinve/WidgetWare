## Run the below build command for first run
# docker-compose build --no-cache airflow
docker-compose build --no-cache airflow
docker-compose up -d postgres 
docker-compose up -d postgres-dbt
docker-compose up airflow