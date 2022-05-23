# Start Redis & PostgreSQL services
docker-compose up  --remove-orphans -d redis mysql
# Wait for services to come up fully...

# Start Superset
docker-compose up -d superset
# Wait for Superset to come up fully...

sleep 60

# Initialize demo
docker-compose exec superset superset-demo

# Play around in demo...

# Bring everything down
#docker-compose down -v