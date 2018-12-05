#!/bin/bash

############## starts the energyweb-client parity with 
############## settings suitable for "chainhammer"-benchmarking

## change this path to point to your energyweb-client-parity
PARITY=../../../github/non-electron/energywebfoundation_energyweb-client/target/release/parity

## simple solution for 0/25 peers issue, by AndreiD see 
## https://github.com/energywebfoundation/energyweb-client/issues/24#issuecomment-399465395
PEERSFILE=tobalaba-peers.txt

## which APIs to open
RPCAPI="web3,eth,personal,net,parity"

## you want to benchmark over a statistically relevant number of transactions
TXQUEUESIZE=20001


$PARITY --chain tobalaba --pruning=archive \
        --geth --rpcapi $RPCAPI \
        --db-compaction=ssd --cache-size=2048 \
        --no-persistent-txqueue --tx-queue-mem-limit=0 --tx-queue-gas=off \
        --tx-queue-per-sender=$TXQUEUESIZE \
        --reserved-peers $PEERSFILE


