# start this with:
#                  networks/subkey_gen-seeds.sh 4
#
# I suggest paritytech makes this whole procedure into a better scripted automatism
# INCL inserting the generated keys into my own chainspec. This is a good start:
#
# version 0.6
# https://github.com/drandreaskrueger/chainhammer/blob/master/networks/subkey_gen-seeds.sh
#
# N.B.: Also see 
# * subkey_keys-from-seeds.sh and 
# * node-template_chainspec-generate.sh and 
# * node-template_start-local-nodes.sh
# * node-template_purge-chains.sh
# * substrate-insert-keys.py

FOLDER=networks/cfg
NUM=$1
if [ -z "$NUM" ] 
then
	echo "give number of nodes as integer arg please"
	exit
fi

# easier to store & recall in bash arrays when using no spaces, instead use hyphens
hyphened2seed (){
    seed=$(echo $1 | sed -r 's/-/ /g' ) # turns the hyphens back into spaces
}

echo generating $NUM seed phrases:
echo
SEEDPHRASES=()
for (( i=1; i<$NUM+1; i++ ));
do
	phrase=$(subkey generate | grep "Secret phrase"  | sed -r 's/`//g' ) # remove the strange `
	phrase=$(echo $phrase | awk '{ print $3 "-" $4 "-" $5 "-" $6 "-" $7 "-" $8 "-" $9 "-" $10 "-" $11 "-" $12 "-" $13 "-" $14 }')
	hyphened2seed $phrase
	echo "$seed"
	SEEDPHRASES+=( $phrase )
done


echo
echo writing secretphrases into files:
echo
for (( i=1; i<$NUM+1; i++ ));
do
    filename=$FOLDER/seed$i.secret
    hyphened2seed ${SEEDPHRASES[$i-1]}
    echo $seed > $filename
    echo $i $filename
done

echo
echo babe and grandpa ADDRESSES for replacing the section in the chainspec.json:
echo
echo "\"babe\"": {"\"authorities\"": [
for (( i=1; i<$NUM+1; i++ ));
do
    hyphened2seed ${SEEDPHRASES[$i-1]}
	address=$(subkey --sr25519 inspect "$seed" | grep "Address" | awk '{ print $3 }')
	printf "["\"$address\"", 1]"
	if [ "$i" -ne "$NUM" ]
	then
		printf ","
	fi
	echo
done
echo ]},

echo "\"grandpa\"": {"\"authorities\"": [
for (( i=1; i<$NUM+1; i++ ));
do
    hyphened2seed ${SEEDPHRASES[$i-1]}
	address=$(subkey --ed25519 inspect "$seed" | grep "Address" | awk '{ print $3 }')
	printf "["\"$address\"", 1]"
	if [ "$i" -ne "$NUM" ]
	then
		printf ","
	fi
	echo
done
echo ]},

echo
echo insert into keystores, beware: 2 validators running with same key, will get you slashed.
echo
for (( i=1; i<$NUM+1; i++ ));
do
    suri=${SEEDPHRASES[$i-1]}
    hyphened2seed $suri
    pubkey_sr25519=$(subkey --sr25519 inspect "$seed" | grep "Public key" | awk '{ print $4 }')
    pubkey_ed25519=$(subkey --ed25519 inspect "$seed" | grep "Public key" | awk '{ print $4 }')
    filename=$FOLDER/seed$i.babegran
    echo $pubkey_sr25519 > $filename
    echo $pubkey_ed25519 >> $filename
    echo $filename
    echo author.insertKey\(\"babe\",\"$seed\",\"$pubkey_sr25519\"\)
    echo author.insertKey\(\"gran\",\"$seed\",\"$pubkey_ed25519\"\)
done

