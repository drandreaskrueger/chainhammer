# for 4 nodes start this:
#                        node-template_start-local-nodes.sh 4
#
# version 0.6
# https://github.com/drandreaskrueger/chainhammer/blob/master/networks/node-template_start-local-nodes.sh

FOLDER=networks/cfg
FILESTUB=CH
CONFIG="--validator --chain "$FOLDER/$FILESTUB"-raw.json --telemetry-url ws://telemetry.polkadot.io:1024"

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
    echo rpc 9933 + 11 = ws 9944 port collision
    echo log file names 01 .. 09 ... 10
    exit
fi


echo
echo now start the network with $NUM interconnected nodes
echo 
echo common configuration:
echo $CONFIG
echo 

name=$FILESTUB"-node-01"
logfile="logs/substrate_"$FILESTUB"01.log"
port=30333
rpcport=9933
wsport=9944
key=$(cat $FOLDER/seed1.secret)
# echo $name $wsport $rpcport $logfile 
 
#--key \"$key\" 
echo node-template --name $name --port $port --rpc-port $rpcport --ws-port $wsport --base-path /tmp/$name $CONFIG
node-template --name $name --port $port --rpc-port $rpcport --ws-port $wsport --base-path /tmp/$name $CONFIG > $logfile  2>&1 &

echo sleep 3 seconds so that the first node has output its identity for sure
sleep 3

identity=$(cat logs/substrate_CH01.log | grep "Local node identity is" | awk '{print $7 }')
bootnode=/ip4/127.0.0.1/tcp/30333/p2p/$identity

echo bootnode: $bootnode
echo 
logfiles="logs/substrate_CH01.log "

for (( i=2; i<$NUM+1; i++ ));
do
    port=$((30332+i))
    rpcport=$((9932+i))
    wsport=$((9943+i))
    logfile="logs/substrate_"$FILESTUB"0"$i".log"
    name=$FILESTUB"-node-0"$i
    # echo $name $port $rpcport $logfile 
    echo node-template --name $name --port $port --rpc-port $rpcport --ws-port $wsport --base-path /tmp/$name $CONFIG --bootnodes $bootnode 
    node-template --name $name --port $port --rpc-port $rpcport --ws-port $wsport --base-path /tmp/$name $CONFIG --bootnodes $bootnode > $logfile  2>&1 &
    logfiles+="$logfile "
done

echo
echo Done. Now insert the babe and grandpa keys. And watch the logs with:
echo tail -f "$logfiles"
echo
