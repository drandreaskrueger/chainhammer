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

# fix versions because otherwise so many problems:
python3 -m pip install --upgrade pip==18.1
pip3 install --upgrade py-solc==3.2.0 web3==4.8.2 web3[tester]==4.8.2 rlp==0.6.0 eth-testrpc==1.3.5 requests==2.21.0 pandas==0.23.4 matplotlib==3.0.2 pytest==4.0.2 pytest-cov==2.6.0 jupyter==1.0.0 ipykernel==5.1.0

# every few months try out newer versions instead:
# python3 -m pip install --upgrade pip
# pip3 install --upgrade py-solc web3 web3[tester] rlp eth-testrpc requests pandas matplotlib pytest pytest-cov jupyter ipykernel
echo 

ipython kernel install --user --name="Python.3.py3eth"
echo

set +x
