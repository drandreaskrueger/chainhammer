echo run all -stop.sh scripts once, patience please
networks/testrpc-stop.sh &> /dev/null
echo 1/4
networks/geth-clique-stop.sh &> /dev/null
echo 2/4
networks/quorum-stop.sh &> /dev/null
echo 3/4
networks/parity-stop.sh &> /dev/null
echo 4/4
echo

echo killing containers, then restarting docker:
sudo docker kill $(sudo docker ps -q)
sudo systemctl restart docker
echo 

echo pkill known runtimes:
sudo pkill bootnode
sudo pkill crux
sudo pkill geth
sudo pkill docker-proxy
sudo pkill docker-compose

echo sleep 2
sleep 2
echo 

echo you might have to manually kill more:
echo
sudo scripts/netstat_port8545.sh
echo
ps aux | grep tps.py | grep -v grep
ps aux | grep crux | grep -v grep
ps aux | grep geth | grep -v grep


