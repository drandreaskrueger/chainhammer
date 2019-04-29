
echo
echo docker
echo will remove: docker docker-engine docker.io
echo then install: docker-ce
echo should you not want that, CTRL-C now, and execute the remaining commands in install.sh manually

echo
if [ "$1" == "ubuntu" ]; then
    echo Your CLI switch: ubuntu
else
    echo no CLI switch, thus using the Debian routine.    
fi
echo


read -p "Press enter to continue"
echo 

echo stopping docker daemon then 
echo remove docker docker-engine docker.io
# possibly not installed, so switch off the trap: 
set +e
sudo service docker stop
sudo apt-get -y remove docker docker-engine docker.io
set -e
echo 

file=/etc/apt/sources.list.d/docker.list
if [ -f "$file" ]
then
    echo making backup of $file because the following command will overwrite that!
    sudo cp $file $file.save
fi


if [ "$1" == "ubuntu" ]; then
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee $file
else
	echo add docker debian gpg key:
	# add key - how more elegant?
	# rm -f gpg 
	# wget "https://download.docker.com/linux/debian/gpg"
	# sudo apt-key add gpg
	# rm gpg
	curl https://download.docker.com/linux/debian/gpg | sudo apt-key add -
	echo new $file
	echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee $file
	echo
fi

set +e
sudo apt-get update
set -e
echo
echo install docker-ce
sudo apt-cache policy docker-ce
sudo apt-get -y install docker-ce 

echo add group docker to current user
sudo usermod -aG docker ${USER}
groups $USER

echo sudo service docker restart
sudo service docker restart
systemctl status docker --no-pager

docker --version

