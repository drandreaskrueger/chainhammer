# defaults:
DBFILE=temp.db
INFOFILE=hammer/last-experiment.json
TPSLOG=logs/tps.py.log
DEPLOYLOG=logs/deploy.py.log
SENDLOG=logs/send.py.log

if [ -z "$CH_TXS" ] || [ -z "$CH_THREADING" ]; then 
    echo "You must set 2 ENV variables, examples:"
    echo "export CH_TXS=1000 CH_THREADING=sequential"
    echo "export CH_TXS=5000 CH_THREADING=\"threaded2 20\""
    exit
fi

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
echo infoword: $INFOWORD
echo number of transactions: $CH_TXS 
echo concurrency algo: $CH_THREADING
echo
echo infofile: $INFOFILE
echo blocks database: $DBFILE
echo log files:
echo $TPSLOG
echo $DEPLOYLOG
echo $SENDLOG
echo

# exit

if (( $# == 2 )); then
    title start network
    source networks/$2-start.sh
    echo
fi


title "activate virtualenv" 
source env/bin/activate
echo
python --version
echo 

cd hammer
rm -f $INFOFILE

title is_up.py
echo Loops until the node is answering on the expected port.
./is_up.py
echo Great, node is available now.
echo 

title tps.py
echo start listener tps.py, show here but also log into file $TPSLOG
echo this ENDS after send.py below writes a new INFOFILE $INFOFILE
unbuffer ./tps.py | tee "../$TPSLOG" &
echo

title sleep 1.5 seconds
echo to have tps.py say its thing before deploy.py starts printing
echo
sleep 1.5
echo 

title deploy.py
echo Deploy the smartContract, deploy.py will then trigger tps.py to START counting. 
echo Logging into file $DEPLOYLOG.
echo 
./deploy.py > "../$DEPLOYLOG"
sleep 0
echo

title send.py
echo Send $CH_TXS transactions with concurrency algo \'$CH_THREADING\', plus possibly wait 10 more blocks.
echo Then send.py triggers tps.py to end counting. Logging all into file $SENDLOG. 
echo

./send.py $CH_TXS $CH_THREADING > "../$SENDLOG"

echo

title "sleep 2"
echo wait 2 second until also tps.py has written its results.
echo
sleep 2
echo


title blocksDB_create.py
echo read blocks from node1 into SQL db
cd ../reader
./blocksDB_create.py $DBFILE ../$INFOFILE
echo

title blocksDB_diagramming.py
echo make time series diagrams from SQL db
./blocksDB_diagramming.py $DBFILE $INFOWORD ../$INFOFILE
echo 

title page_generator.py
./page_generator.py ../$INFOFILE ../$TPSLOG
echo 

cd ..

# switch off the trap, because sometimes the 2nd kill in networks/$2-stop.sh is not needed anymore:
set +e
trap '' EXIT

if (( $# == 2 )); then
    title stop network
    source networks/$2-stop.sh
    # sleep 0
    # echo should be stopped now
    # scripts/netstat_port8545.sh
    echo
fi

title "Ready."
echo See that image, and those .md and .html pages.
echo


