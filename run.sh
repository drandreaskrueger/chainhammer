echo 
echo =============================
echo = chainhammer - example run =
echo =============================
echo 
echo study this, to understand the moving parts of chainhammer
echo to run it yourself with variations of network and parameters
echo 
echo start like this:
echo 
echo "    source env/bin/activate"
echo "    unbuffer testrpc-py &> tests/logs/testrpc-py.log &"
echo "    ./run.sh"
echo
echo

echo virtualenv 
source env/bin/activate
echo
echo 

echo start listener tps.py, log into file log/tps.py.log
# ./tps.py
# TODO how to kill this when the below finished plus 10 extra blocks?
echo
echo 

echo smartContract deploy.py, log into file log/deploy.py.log
# it writes a file which triggers the wait loop in tps.py to end
# ./deploy.py
echo
echo

echo hammer transactions send.py, log into file log/send.py.log
# ./send.py threaded2 23
# TODO write blockFrom and blockTo into file, for diagrams
echo
echo

echo show the listener output on screen:
# tail -f log/tps.py.log
# TODO how to kill this and CONTINUE when the above finished?
#
echo
echo

echo read blocks from node1 into SQL db
# cd chainreader
# ./blocksDB_create.py temp.db
echo
echo

echo make time series diagrams from SQL db
# ./blocksDB_diagramming.py temp.db TEMP
# TODO pass in exact blocknumbers of experiment
echo
echo

