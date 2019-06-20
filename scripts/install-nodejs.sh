NODE_VERSION="10"

echo
echo installing nodejs version $NODE_VERSION and npm, 
echo and setting global installs into ~/.npm-global
echo
echo read script before run, you might not want this.
echo
read -p "Press enter to continue"


echo 
echo set repo source and sudo apt update:
curl -sL https://deb.nodesource.com/setup_$NODE_VERSION.x | sudo bash -

echo install dependencies
sudo apt-get install -y gcc g++ make nodejs git

echo install npm
curl -L https://npmjs.org/install.sh | sudo bash

# On Debian I had EACCES access rights problems 
# and actually for 4 ways of npm install: 
# npm i $PRG
# npm i -g $PRG
# sudo npm i $PRG
# sudo npm i -g $PRG 
# = all 4 had -different- EACCESS problems!
# until I used this:

mkdir -p ~/.npm-global
sudo chown -R $USER ~/.npm-global
npm config set prefix '~/.npm-global'

echo "export PATH=\$PATH:~/.npm-global/bin" >> ~/.profile
export PATH=$PATH:~/.npm-global/bin

echo
echo ready
echo

set -x
npm --version
nodejs --version
node --version
set +x



