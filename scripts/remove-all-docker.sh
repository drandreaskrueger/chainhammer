
if [ "$1" == "silent" ]; then
    echo Skipping warning - will directly remove all docker containers and images!
    echo 
else
    echo
    echo kill and remove all docker containers and instances
    echo careful!
    echo especially if you still need the DATA in your docker containers
    echo this could turn out to be tragic
    echo 
    read -p "Press enter to continue"
    echo
fi
 
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)