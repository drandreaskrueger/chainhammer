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

title "chainhammer - example run ="

echo 
echo study this, to understand the moving parts of chainhammer
echo to run it yourself with variations of network and parameters
echo 
echo start e.g. with testrpc as Ethereum network:
echo 
echo "    source env/bin/activate"
echo "    unbuffer testrpc-py &> tests/logs/testrpc-py.log &"
echo
echo "    ./run.sh"
echo
echo

# Later: read parameters from file
# source $1
SEND_PARAMS="threaded2 20"
SEND_PARAMS="sequential"
DBFILE=temp.db
INFOFILE=../hammer/last-experiment.json
TPSLOG=logs/tps.py.log
PREFIX=Geth-Local


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
echo send many transactions, plus wait 10 more blocks, log into file logs/send.py.log. Then this triggers tps.py to end counting.
echo
./send.py $SEND_PARAMS > "../logs/send.py.log"
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
./blocksDB_diagramming.py $DBFILE $PREFIX $INFOFILE

title page_generator.py
./page_generator.py $INFOFILE ../$TPSLOG

title "Ready."
echo See that image, and those .md and .html pages.

trap '' EXIT

cd ..