echo killing containers, then restarting docker:
sudo docker kill $(sudo docker ps -q)
sudo systemctl restart docker
echo 

echo run all -stop.sh and -clean.sh scripts once, patience please
networks/testrpc-stop.sh &> /dev/null
networks/testrpc-clean.sh > /dev/null
echo 1/4 done
networks/geth-clique-stop.sh &> /dev/null
networks/geth-clique-clean.sh &> /dev/null
echo 2/4 done
networks/quorum-stop.sh &> /dev/null
networks/quorum-clean.sh &> /dev/null
echo 3/4 done
networks/parity-stop.sh &> /dev/null
networks/parity-clean.sh &> /dev/null
echo 4/4 done
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

echo or simply look around with: ps aux

