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

