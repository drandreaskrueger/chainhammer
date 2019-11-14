# for 4 nodes start this:
#                        node-template_purge-chains.sh 4
#
# version 0.6
# https://github.com/drandreaskrueger/chainhammer/blob/master/networks/node-template_purge-chains.sh

FOLDER=networks/cfg
FILESTUB=CH
CHAIN="$FOLDER/$FILESTUB"-raw.json

NUM=$1
if [ -z "$NUM" ] 
then
    echo "give number of nodes as integer arg please"
    exit
fi
if [ "$NUM" -ge 10 ] 
then
    echo "max number of nodes is 9, then it would need some tiny code upgrades:"
    echo e.g.
    echo log file names 01 .. 09 ... 10
    exit
fi

echo
echo Be aware this might cause problems if nodes are still running.
echo

for (( i=1; i<$NUM+1; i++ ));
do
    name=$FILESTUB"-node-0"$i
    echo node-template purge-chain -y --chain=$CHAIN --base-path /tmp/$name
    node-template purge-chain -y --chain=$CHAIN --base-path /tmp/$name
done


