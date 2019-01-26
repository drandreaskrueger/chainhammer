
# two CLI switches:
#
# scripts/remove-all-docker.sh = shows initial warning and waits for pressing enter
# scripts/remove-all-docker.sh silent = does not wait for confirmation
# scripts/remove-all-docker.sh non/silent keep-images = skips: docker rmi ...  

if [ "$1" == "silent" ]; then
    echo Skipping warning - will directly remove all docker containers and images!
    echo 
else
    echo
    echo kill and remove all docker containers and instances - careful!
    echo especially if you still need the DATA in your docker containers
    echo this could turn out to be tragic. Rather exit now, and check.
    echo 
    read -p "Press enter to continue"
    echo
fi
 
REMOVE=$(docker ps -q)
if [ "$REMOVE" != "" ]; then
    echo docker kill $REMOVE
    docker kill $REMOVE
else
    echo no docker processes, nothing to kill.
fi


REMOVE=$(docker ps -q -a)
if [ "$REMOVE" != "" ]; then
    echo docker rm  $REMOVE
    docker rm $REMOVE
else
    echo no docker containers, nothing to remove.
fi


if [ "$2" == "keep-images" ]; then
    echo keep-images = skip removing the docker images
else
    REMOVE=$(docker images -q)
    if [ "$REMOVE" != "" ]; then
        echo docker rmi  $REMOVE
        docker rmi $REMOVE
    else
        echo no docker images, nothing to remove.
    fi
fi

echo