echo
echo first initialization
echo 

echo make logs and runs folder
mkdir -p logs
mkdir -p results/runs
echo 

echo start virtualenv
source env/bin/activate
echo

echo start testRPC ethereum provider
networks/testrpc-start.sh
echo 

echo deploy smart contract to test installation, connection, and create essential files  
cd hammer
touch account-passphrase.txt
./deploy.py andtests
cd ..
echo

echo stop testRPC ethereum provider
networks/testrpc-stop.sh
echo 
