# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT
#
#
#
#
#
# N.B.: This script is very new, 
# and only tested on one local Debian machine;
# not yet in the cloud or on differently configured machines.
#  
# Please provide detailed feedback if ANYTHING goes wrong.
# Just raise an issue in the chainhammer repo on github.com
# Thanks.
#
#
#
#
#
echo 
echo Install ChainHammer dependencies, and clone network starter repos
echo version v44
echo 
echo Please report any problems if this script is NOT ending with: 
echo ... with exit code 0.
echo
echo Warning: No guarantees!! 
echo Executing this script has consequences for this machine.
echo Better only use on a disposable/cloud/virtualbox machine, 
echo and NOT on your main work machine!!
echo 
echo Is this the \"chainhammer\" folder where you want everything installed?
echo $(pwd)
echo
read -p "Press enter to continue"
echo
echo must install some tools on system level, please input your sudo password:
sudo echo
echo got sudo, thanks.
echo 
echo sudo apt-get update
echo  
set +e # don't trap this, there are frequent errors
sudo apt-get update
set -e
echo 
PACKAGES="wget htop jq apt-transport-https ca-certificates wget software-properties-common python3-pip libssl-dev expect-dev"
echo installing $PACKAGES
sudo apt-get install -y 

echo
echo
echo docker
echo will remove: docker docker-engine docker.io
echo then install: docker-ce
echo should you not want that, CTRL-C now, and execute the remaining commands in install.sh manually
read -p "Press enter to continue"

echo 
sudo apt-get -y remove docker docker-engine docker.io

# add key - how more elegant?
rm -f gpg 
wget "https://download.docker.com/linux/debian/gpg"
sudo apt-key add gpg
rm gpg


echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee -a /etc/apt/sources.list.d/docker.list
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



echo
echo install solidity compiler solc into /usr/local/bin/
echo 
read -p "Press enter to continue"

# someone should PLEASE create a Debian specific installation routine
# see https://solidity.readthedocs.io/en/latest/installing-solidity.html 
# and https://github.com/ethereum/solidity/releases
wget https://github.com/ethereum/solidity/releases/download/v0.4.24/solc-static-linux
chmod 755 solc-static-linux 
echo I hope /usr/local/bin/ is in your PATH?
echo $PATH
sudo mv solc-static-linux /usr/local/bin/
sudo ln -s -f /usr/local/bin/solc-static-linux /usr/local/bin/solc
solc --version


echo
echo installing go and geth
echo 
read -p "Press enter to continue"

# would be nice to simply use geth via docker
# but this does not work yet:
# docker run ethereum/client-go attach https://localhost:8545
# please help
# until then, compile and install locally:

echo 
INSTALLER="go1.11.linux-amd64.tar.gz"
echo install go $INSTALLER
rm -f $INSTALLER
wget https://dl.google.com/go/$INSTALLER
sudo tar -C /usr/local -xzf $INSTALLER 
rm $INSTALLER  
mkdir -p ~/go/bin
echo "export PATH=\$PATH:/usr/local/go/bin:~/go/bin" >> ~/.profile
export PATH=$PATH:/usr/local/go/bin:~/go/bin
go version

    

echo install geth
go get -d github.com/ethereum/go-ethereum
go install "github.com/ethereum/go-ethereum/cmd/geth"
geth version




FOLDER=./networks/repos/
echo 
echo network starters
echo will be installed into $FOLDER
echo below here
echo $(pwd)
echo
echo careful - whatever was in those subfolders will be gone after this!
read -p "Press enter to continue"

mkdir -p $FOLDER
cd $FOLDER

echo 
echo paritytech/parity-deploy
rm -rf paritytech_parity-deploy
git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy

echo
rm -rf drandreaskrueger_geth-dev
echo javahippie/geth-dev my configured fork drandreaskrueger/geth-dev 
git clone https://github.com/drandreaskrueger/geth-dev.git drandreaskrueger_geth-dev

echo 
echo blk-io/crux
rm -rf blk-io_crux
git clone  https://github.com/blk-io/crux blk-io_crux
cd blk-io_crux
git checkout f39db2345cf9d82e76d3905468e6e5ea1469b09d
cd ..

cd ../..


echo
echo
echo

scripts/install-virtualenv.sh

echo
echo Done. All is good if it says: filed with exit code 0. 
echo
