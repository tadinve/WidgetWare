# Base Image
FROM python:3.7-slim-bullseye
LABEL maintainer="Venkat"

# Arguments that can be set with docker build
ARG AIRFLOW_VERSION=2.2.4
ARG AIRFLOW_HOME=/opt/airflow

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Install dependencies and tools
RUN apt-get update -y && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    python3-dev \
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev libpq-dev \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    netcat \
    && apt-get autoremove -yqq --purge && apt-get clean

# Upgrade pip
# Create airflow user 
# Install apache airflow with subpackages
RUN pip install --upgrade "pip==20.2.4" && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow==${AIRFLOW_VERSION} --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.2.4/constraints-3.7.txt && \
    pip install apache-airflow-providers-postgres==4.1.0 && \
    pip install apache-airflow-providers-apache-hdfs==2.1.0 && \
    pip install apache-airflow-providers-apache-hive==2.0.2 && \
    pip install apache-airflow-providers-apache-spark==2.0.1 && \
    pip install apache-airflow-providers-slack==4.0.1 && \
    pip install apache-airflow-providers-amazon==3.3.0 && \
    pip install apache-airflow-providers-http==2.0.1 && \ 
    pip install psycopg2 && \
    pip install pandas

RUN pip install --upgrade "protobuf<=3.20.1"

RUN pip install scipy && \
    pip install great_expectations && \
    pip install dbt-postgres

# Copy the airflow.cfg file (config)
#COPY ./config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Set the owner of the files in AIRFLOW_HOME to the user airflow
RUN chown -R airflow: ${AIRFLOW_HOME}

# Copy the entrypoint.sh from host to container (at path AIRFLOW_HOME)
COPY ./start-airflow.sh ./start-airflow.sh

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Set the entrypoint.sh file to be executable
RUN chmod +x ./start-airflow.sh

# Set the username to use
#USER airflow
USER root

# Create the folder dags & logs inside $AIRFLOW_HOME
RUN mkdir -p ${AIRFLOW_HOME}/dags
RUN mkdir -p ${AIRFLOW_HOME}/plugins
RUN mkdir -p ${AIRFLOW_HOME}/logs 
RUN mkdir -p ${AIRFLOW_HOME}/logs/webserver
RUN mkdir -p ${AIRFLOW_HOME}/logs/scheduler

RUN echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > ${AIRFLOW_HOME}/.env


# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080

RUN airflow users create \
            --username admin \
            --firstname Admin \
            --lastname Account \
            --role Admin \
            --email admin@admin.com \
            --password admin

# Execute start-airflow.sh
CMD [ "./start-airflow.sh" ]

    