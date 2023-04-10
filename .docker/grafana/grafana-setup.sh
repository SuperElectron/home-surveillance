
## Run this script from the same directory

# If running this script before logging into grafana, do not pass arguments
## example usage: ./grafana-setup.sh
# If you have already logged in, then pass username & password
## example usage: ./grafana-setup.sh <username> <password>

USER=$1
PASSWORD=$2

if [ -z "$USER" ]; then
  USER=admin
  PASSWORD=admin
  echo "Setting user to default login"
fi

echo "Credentials have been set: user=${USER}, password=${PASSWORD}"
echo "Creating Ant Media Server Grafana Panel"
curl -s "http://172.23.0.10:3000/api/dashboards/db" \
        -u "${USER}:${PASSWORD}" \
        -H "Content-Type: application/json" \
        --data-binary "@dashboard.json"

echo "Creating Elastich Search DataSource for Ant Media Server Grafana Panel"
curl -s -X "POST" "http://172.23.0.10:3000/api/datasources" \
        -H "Content-Type: application/json" \
        -u "${USER}:${PASSWORD}" \
        --data-binary "@datasource.json"
