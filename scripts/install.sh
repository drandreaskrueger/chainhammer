# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo; echo "\"${last_command}\" command filed with exit code $?."' EXIT
#
#
# scripts/install.sh                    # Debian, including all
# scripts/install.sh docker ubuntu      # Ubuntu, including all
# scripts/install.sh nodocker           # Debian/Ubuntu, no docker no network starters
#
#
# N.B.: These install-XYZ.sh scripts are very new, 
# and have mainly been tested on Debian machines.
#  
# Please provide detailed feedback if ANYTHING goes wrong on your machine.
# Just raise an issue in the chainhammer repo on github.com
# Thanks.
#
#

function install_chapter {
    echo 
    echo ==========================================
    echo = $1
    echo ==========================================
        
    source $1
}

echo 
echo ===================================================================
echo Install ChainHammer dependencies, and clone network starter repos
echo version v59
echo ===================================================================
echo 
echo Please report any issues IF this script is NOT ending with: 
echo ... with exit code 0.
echo
echo Warning: No guarantees!! 
echo Executing this script has consequences for this machine.
echo Better only use on a disposable/cloud/virtualbox machine, 
echo and NOT on your main work machine!!
echo
if [ "$1" == "nodocker" ]; then
    echo Your CLI switch: Do NOT install docker, and network starters!
    echo
fi
echo 
echo Is this the \"chainhammer\" folder where you want everything installed?
echo $(pwd)
echo
read -p "Press enter to continue"
echo
echo must install some tools on system level, please input your sudo password:
sudo ls scripts/install-*.sh
echo got sudo, thanks.


#
# Here is where the magic happens:
#

# sudo apt install ...
install_chapter scripts/install-packages.sh

# parity-deploy, geth-dev, and quorum-crux:
if [ "$1" == "nodocker" ]; then
    echo ====================================================== 
    echo Skipping docker, docker-compose, and network-starters.
    echo ====================================================== 
else
    install_chapter "scripts/install-docker.sh $2"
    install_chapter scripts/install-docker-compose.sh
    install_chapter scripts/install-network-starters.sh
fi

# solc    
install_chapter scripts/install-solc.sh

# geth
install_chapter scripts/install-geth.sh

# env
install_chapter scripts/install-virtualenv.sh

# deploy.py andtests on testRPC
install_chapter scripts/install-initialize.sh


echo
echo Done. All is good if it says: filed with exit code 0. 
echo
echo N.B.: You might need to LOGOUT and LOGIN before docker starts working for you!
echo  
