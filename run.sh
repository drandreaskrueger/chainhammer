if (( $# != 1  && $# != 2 )); then
    echo "Syntax:"
    echo "./run.sh info-word [network-scripts-prefix]"
    echo "e.g."
    echo "./run.sh Geth-t2.xlarge"
    echo "./run.sh Geth-t2.xlarge geth-clique"
    echo "The first case assumes that network nodes are started manually."
    exit    
fi

INFOWORD=$1

# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo; echo "\"${last_command}\" command filed with exit code $?."' EXIT
#

function title {
    echo =============================
    echo = $1
    echo ============================= 
}  

echo 

title "chainhammer v52 - run all ="

echo 
echo study this, to understand the moving parts of chainhammer
echo to run it yourself with variations of network and parameters
echo 
echo start e.g. with testrpc as Ethereum network:
echo 
echo "    source env/bin/activate"
echo "    unbuffer testrpc-py &> tests/logs/testrpc-py.log &"
echo
echo "    ./run.sh TestRPC-local"
echo
echo

# defaults:
DBFILE=temp.db
INFOFILE=../hammer/last-experiment.json
TPSLOG=logs/tps.py.log

NUM_TRANSACTIONS=1000

# fallback is non-async sending
# important especially for testrpc-py which does not handle multithreading well
# can be overwritten by the specific network starter
SEND_PARAMS="threaded2 20"
SEND_PARAMS="sequential"

if (( $# == 2 )); then
    title start network
    source networks/$2-start.sh
fi


title "activate virtualenv" 
source env/bin/activate
echo
echo 

cd hammer
rm -f $INFOFILE

title is_up.py
echo Loops until the node is answering on the expected port.
./is_up.py
echo Great, node is available now.
echo 
echo

title tps.py
echo start listener tps.py, show here but also log into file $TPSLOG
echo this ends after send.py below writes a new INFOFILE.
unbuffer ./tps.py | tee "../$TPSLOG" &

sleep 1.5 # to have tps.py say its thing before deploy.py is printing
echo
echo 

title deploy.py
echo smartContract deploy.py, log into file logs/deploy.py.log. This triggers tps.py to start counting.
./deploy.py > "../logs/deploy.py.log"
sleep 0
echo
echo

title send.py
echo Send $NUM_TRANSACTIONS transactions with algo \'$SEND_PARAMS\', plus possibly wait 10 more blocks.
echo Logging into file logs/send.py.log. Then this triggers tps.py to end counting.
echo
./send.py $NUM_TRANSACTIONS $SEND_PARAMS > "../logs/send.py.log"
echo
echo

title "sleep 1"
echo wait 1 second until also tps.py has written its results.
echo
sleep 1
echo
echo


title blocksDB_create.py
echo read blocks from node1 into SQL db
cd ../reader
./blocksDB_create.py $DBFILE $INFOFILE
echo
echo

title blocksDB_diagramming.py
echo make time series diagrams from SQL db
./blocksDB_diagramming.py $DBFILE $INFOWORD $INFOFILE

title page_generator.py
./page_generator.py $INFOFILE ../$TPSLOG

cd ..

if (( $# == 2 )); then
    title stop network
    source networks/$2-stop.sh
fi


title "Ready."
echo See that image, and those .md and .html pages.

trap '' EXIT

