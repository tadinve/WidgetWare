docker-compose up -d apache-superset

sleep 30

docker exec apache-superset /bin/sh -c  "./app/initialize-superset.sh"