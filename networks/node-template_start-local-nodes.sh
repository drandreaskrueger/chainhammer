# for 4 nodes start this:
#                        node-template_start-local-nodes.sh 4
#
# version 0.4
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
    echo "max number of nodes is 9, then it would need some tiny code upgrades"
    exit
fi


echo
echo now start the network with $NUM interconnected nodes
echo 
echo common configuration:
echo $CONFIG

node-template --name CH-node-01 --port 30333 --base-path /tmp/CH-node-01 $CONFIG --node-key $(cat networks/cfg/seed1.secret) > logs/substrate_CH01.log  2>&1 &

echo sleep 3 seconds so that the first node has output its identity for sure
sleep 3

identity=$(cat logs/substrate_CH01.log | grep "Local node identity is" | awk '{print $7 }')
bootnode=/ip4/127.0.0.1/tcp/30333/p2p/$identity

echo bootnode: $bootnode
echo 
logfiles="logs/substrate_CH01.log "

for (( i=2; i<$NUM+1; i++ ));
do
    port=$((33332+i))
    logfile="logs/substrate_CH0"$i".log"
    key=$(cat "networks/cfg/seed"$i".secret")
    name=$FILESTUB"-node-0"$i
    echo $name $port $key $logfile 
    node-template --name $name --port $port --base-path /tmp/$name $CONFIG --node-key $key --bootnodes $bootnode > $logfile  2>&1 &
    logfiles+="$logfile "
done

echo Done. Watch the logs with:
echo tail -f "$logfiles"