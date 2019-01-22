#!/bin/bash

FOLDER=networks/repos/blk-io_crux/docker/quorum-crux
GETBACK=../../../../..

echo configure quorum

cd $FOLDER

echo git checkout a version that definitely worked and included my patches
echo git checkout eeb63a91b7eda0180c8686f819c0dd29c0bc4d46
git checkout eeb63a91b7eda0180c8686f819c0dd29c0bc4d46

# nice: blk-io merged my patches into 
# https://github.com/blk-io/crux/commit/ddd126e62f1f0dac341b2b61b01688f1d960dbd2
# echo patch: raise gasLimit
# jq '.gasLimit = "0x1312D00"' istanbul-genesis.json > tmp && mv tmp istanbul-genesis.json
# echo patch: larger txpool, blockperiod 1 second
# sed -i 's/PRIVATE_CONFIG/ARGS=$ARGS"--txpool.globalslots 50000 --txpool.globalqueue 50000 --istanbul.blockperiod 1 "\nPRIVATE_CONFIG/g' istanbul-start.sh

echo patch: port 22001 change to 8545
sed -i 's/22001:22000/8545:22000/g' docker-compose-local.yaml

cd $GETBACK
