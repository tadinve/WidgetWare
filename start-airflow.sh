## Run the below build command for first run

docker-compose build airflow
docker-compose up -d postgres 
docker-compose up -d postgres-dbt
docker-compose up -d airflow