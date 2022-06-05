# WidgetWare



## Airflow

### Please use the below commands to just start airflow docker 
* Airflow container internally initializes dbt and also great_expectations as pip packages

#### 1. Build Airflow
> cd WidgetWare && docker-compose build --no-cache airflow

#### 2. Start Airflow
> ./start-airflow-docker.sh


#### 3. Stop Airflow
> ./stop-airflow-docker.sh



## Superset

### Please use the below commands to just start apache superset docker 
* Superset docker-compose file also utilizes redis and mysql for backend and cache functionalities

#### 1. Start Superset
> cd WidgetWare/docker/superset && ./start_superset.sh


#### 3. Stop Airflow
> ./stop_superset.sh
