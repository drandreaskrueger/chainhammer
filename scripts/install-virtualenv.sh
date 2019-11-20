echo
echo create chainhammer virtualenv
echo
echo after possibly removing a whole existing env/ folder !!!
echo 
echo the new virtualenv will be installed below here:
echo $(pwd)
echo 
read -p "Think twice. Then press enter to continue"
echo

# this is for the tools not from pypi but via setup.py
FOLDER=./networks/repos/

set -x
# sudo pip3 install virtualenv # installation of virtualenv tool moved to install-packages.sh now
# echo

rm -rf env 
python3 -m venv env
echo

set +x
echo +++ source env/bin/activate
source env/bin/activate
set -x
echo

# fix specific versions - because otherwise sooo many problems:
python3 -m pip install --upgrade pip==19.3.1
pip3 install wheel==0.33.6
pip3 install --upgrade rlp==0.6.0 eth-testrpc==1.3.5 eth-account==0.3.0 web3==4.9.2 web3[tester]==4.9.2 ipykernel==5.1.3 jupyter==1.0.0 matplotlib==3.1.1 pandas==0.25.3 py-solc==3.2.0 pytest==5.3.0 pytest-cov==2.8.1 requests==2.22.0 xxhash==1.4.3 websockets==6.0

# every few months try out newer versions instead:
# python3 -m pip install --upgrade pip
# pip3 install wheel
# eth-testrpc is EOLIFE, TODO: replace with something else; until then, this is obligatory. And stay <v5 for web3 until time for full testing.
# pip3 install --upgrade rlp==0.6.0 eth-testrpc==1.3.5 eth-account==0.3.0 web3==4.9.2 web3[tester]==4.9.2
# BUT find newer versions for these:
# pip3 install --upgrade py-solc requests pandas matplotlib pytest pytest-cov jupyter ipykernel xxhash websockets
echo 

ipython kernel install --user --name="Python.3.py3eth"
echo

echo now install more tools, not on pypi.org yet, i.e. via setup.py
echo
OLDPATH=$(pwd)
cd $FOLDER

echo polkascan/py-scale-codec
rm -rf polkascan_py-scale-codec
git clone https://github.com/polkascan/py-scale-codec polkascan_py-scale-codec
cd polkascan_py-scale-codec
git checkout ce10e0488a7d2a274273f19b079959494032bdf5
python ./setup.py install
cd ..

echo polkascan/py-substrate-interface
rm -rf polkascan_py-substrate-interface
git clone https://github.com/polkascan/py-substrate-interface.git polkascan_py-substrate-interface
cd polkascan_py-substrate-interface 
git checkout ac8ce4a44b5bffcdbce76e843b2e4991cc44b458
python ./setup.py install
cd ..

cd $OLDPATH

set +x
