echo
echo
echo create chainhammer virtualenv
echo
echo after possibly removing a whole existing env/ folder !!!
echo 
echo the new virtualenv will be installed here:
echo $(pwd)
echo 
read -p "Think twice. Then press enter to continue"
echo

set -x
sudo pip3 install virtualenv

rm -rf env 
virtualenv -p python3 env

source env/bin/activate

python3 -m pip install --upgrade pip==18.0
pip3 install --upgrade py-solc==3.1.0 web3==4.7.2 web3[tester]==4.7.2 rlp==0.6.0 eth-testrpc==1.3.5 requests==2.19.1 pandas==0.23.4 matplotlib==3.0.0 pytest pytest-cov jupyter ipykernel
ipython kernel install --user --name="Python.3.py3eth"

set +x