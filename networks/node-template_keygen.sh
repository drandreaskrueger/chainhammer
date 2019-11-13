# start this with:
#                  networks/node-template_keygen.sh 4
#
# I suggest paritytech makes this whole procedure into a better scripted automatism
# INCL inserting the generated keys into my own chainspec. This is a good start:
#
# version 0.4
# https://github.com/drandreaskrueger/chainhammer/blob/master/networks/node-template_keygen.sh

FOLDER=networks/cfg
NUM=$1
if [ -z "$NUM" ] 
then
	echo "give number of nodes as integer arg please"
	exit
fi

hyphened2seed (){
    seed=$(echo $1 | sed -r 's/-/ /g' ) # turn the hyphens back into spaces
}

echo generating $NUM seed phrases:
echo
SEEDPHRASES=()
for (( i=1; i<$NUM+1; i++ ));
do
	phrase=$(subkey generate | grep "Secret phrase"  | sed -r 's/`//g' ) # remove the strange ` completely
	# easier to store & recall in bash arrays when using no spaces, instead use hyphens:
	phrase=$(echo $phrase | awk '{ print $3 "-" $4 "-" $5 "-" $6 "-" $7 "-" $8 "-" $9 "-" $10 "-" $11 "-" $12 "-" $13 "-" $14 }')
	hyphened2seed $phrase
	echo "$seed"
	SEEDPHRASES+=( $phrase )
done


echo
echo writing secrets into files:
echo
for (( i=1; i<$NUM+1; i++ ));
do
    hyphened2seed ${SEEDPHRASES[$i-1]}
    secret=$(subkey --ed25519 inspect "$seed"  | grep "Secret seed" | awk '{ print $3 }')
    filename=$FOLDER/seed$i.secret
    echo $secret > $filename
    echo $i $secret $filename
done

echo
echo babe and grandpa for replacing the section in the chainspec.json:
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

