sudo pkill docker-proxy
sudo pkill bootnode
sudo pkill docker-compose

echo
echo you might have to manually kill more:

sudo scripts/netstat_port8545.sh

echo
ps aux | grep tps.py | grep -v grep


