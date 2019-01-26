DOCKER_COMPOSE_VERSION=1.22.0

echo
echo install docker-compose version $DOCKER_COMPOSE_VERSION
read -p "Press enter to continue"

sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod 755 /usr/local/bin/docker-compose

docker --version
docker-compose --version
