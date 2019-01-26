#
#
# no warning, the name kill- should tell it all, right?
#
#
# so ... read this before you execute it!
#

echo remove all docker, then restarting docker:
scripts/remove-all-docker.sh silent keep-images

echo docker system prune
docker system prune -f

echo sudo service docker restart
sudo service docker restart
sudo systemctl --no-pager status docker
echo 

echo run all -clean.sh scripts once, patience please
networks/testrpc-clean.sh > /dev/null
echo 1/4 done
networks/geth-clique-clean.sh &> /dev/null
echo 2/4 done
networks/quorum-clean.sh &> /dev/null
echo 3/4 done
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

scripts/show-leftovers.sh
