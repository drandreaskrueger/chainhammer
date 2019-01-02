
echo
echo
echo docker
echo will remove: docker docker-engine docker.io
echo then install: docker-ce
echo should you not want that, CTRL-C now, and execute the remaining commands in install.sh manually

read -p "Press enter to continue"
echo 

echo remove docker docker-engine docker.io
# possibly not installed, so switch off the trap: 
set +e
sudo apt-get -y remove docker docker-engine docker.io
set -e

echo add docker debian gpg key:
# add key - how more elegant?
# rm -f gpg 
# wget "https://download.docker.com/linux/debian/gpg"
# sudo apt-key add gpg
# rm gpg
curl https://download.docker.com/linux/debian/gpg | sudo apt-key add -


echo making backup of /etc/apt/sources.list.d/docker.list because the following command will overwrite that!
sudo cp /etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/docker.list.save

echo new /etc/apt/sources.list.d/docker.list
echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
set +e
sudo apt-get update
set -e
sudo apt-cache policy docker-ce
sudo apt-get -y install docker-ce 
sudo systemctl start docker
sudo usermod -aG docker ${USER}
groups $USER

echo 
echo 
echo install docker-compose new version
read -p "Press enter to continue"

sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod 755 /usr/local/bin/docker-compose

echo docker and docker-compose versions:
docker --version
docker-compose --version
