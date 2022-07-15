FROM apache/superset

USER root

# Initialize the database
RUN superset db upgrade
RUN superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin


# Create default roles and permissions
RUN superset init

# Import datasources and dashboards
WORKDIR /home
COPY superset_data/datasources.yml datasources.yml
COPY superset_data/dashboards.yml dashboards.yml
# RUN superset import_datasources -p superset_data/datasources.yml
RUN superset import_datasources -p datasources.yml
RUN superset import_dashboards -p dashboards.yml