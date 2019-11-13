# start this with:
#                  networks/subkey_keys-from-seeds.sh 4
#
# preparation to insert the generated keys into my own chainspec with jq
#
# version 0.4
# https://github.com/drandreaskrueger/chainhammer/blob/master/networks/subkey_keys-from-seeds.sh

FOLDER=networks/cfg
NUM=$1
if [ -z "$NUM" ] 
then
    echo "give number of nodes as integer arg please"
    exit 128
fi

if [ "$2" = "babe" ]; then
    CRYPTOGRAPHY=--sr25519
fi
if [ "$2" = "grandpa" ]; then
    CRYPTOGRAPHY=--ed25519
fi

if [ -z "$CRYPTOGRAPHY" ]; then
    echo "must specify babe or grandpa as 2nd arg"
    exit
fi

printf "["
for (( i=1; i<$NUM+1; i++ ));
do
    filename=$FOLDER/seed$i.secret
    secret=$(cat $filename) 
    # echo $secret 
    address=$(subkey $CRYPTOGRAPHY inspect "$secret" | grep "Address" | awk '{ printf $3 }')
    printf "["\"$address\"",1]"
    if [ "$i" -ne "$NUM" ]
    then
        printf ","
    fi
done
printf "]"
