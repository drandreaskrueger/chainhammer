echo
echo first initialization
echo 

echo make logs folder
mkdir -p logs
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
