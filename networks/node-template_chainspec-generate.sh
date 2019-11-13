# for 4 nodes start this:
#                        node-template_chainspec-generate.sh 4
#
# version 0.4
# https://github.com/drandreaskrueger/chainhammer/blob/master/networks/node-template_chainspec-generate.sh

FOLDER=networks/cfg
FILESTUB=CH
TEMPLATE="local"
NUM=$1
if [ -z "$NUM" ] 
then
	echo "give number of nodes as integer arg please"
	exit
fi

echo 
echo make $NUM keys:
networks/subkey_gen-seeds.sh $1

echo 
filename_orig=$FOLDER/$TEMPLATE.json
echo generating from template \'$TEMPLATE\' the file: $filename_orig 
node-template build-spec --chain $TEMPLATE > $filename_orig
wc $filename_orig

echo
filename_my_chainspec=$FOLDER/$FILESTUB.json
echo swapping out babe and grandpa from that json file, into new file $filename_my_chainspec
# this line is good for debugging as it outputs .genesis.runtime.{babe,grandpa} to stdout:
# jq '.genesis.runtime.babe.authorities='$(networks/subkey_keys-from-seeds.sh $NUM babe) networks/cfg/local.json | jq '.genesis.runtime.grandpa.authorities='$(networks/subkey_keys-from-seeds.sh $NUM grandpa) | jq '.genesis.runtime.grandpa,.genesis.runtime.babe'
jq '.genesis.runtime.babe.authorities='$(networks/subkey_keys-from-seeds.sh $NUM babe) $filename_orig | jq '.genesis.runtime.grandpa.authorities='$(networks/subkey_keys-from-seeds.sh $NUM grandpa) > $filename_my_chainspec
wc $filename_my_chainspec

echo
filename_my_raw=$FOLDER/$FILESTUB-raw.json
echo transforming that file into "raw" chainspec file $filename_my_raw
node-template build-spec --chain $TEMPLATE --raw > $filename_my_raw
wc $filename_my_raw

echo
echo visual check intermediate file - here .genesis.runtime.grandpa :
jq '.genesis.runtime.grandpa' $filename_my_chainspec

echo
echo Done.
