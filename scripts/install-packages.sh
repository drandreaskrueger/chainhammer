echo 
echo sudo apt-get update
echo  
set +e # don't trap this, there are frequent errors
sudo apt-get update
set -e
echo 
PACKAGES="wget htop jq apt-transport-https ca-certificates wget software-properties-common python3-pip python3-virtualenv libssl-dev expect-dev dbus-x11 terminator"
echo installing $PACKAGES
sudo apt-get install -y $PACKAGES 

echo
echo packages install ready.
echo
