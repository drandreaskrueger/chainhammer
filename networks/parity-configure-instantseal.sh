#!/bin/bash

# PARITY_ARGS="--config dev --geth --gasprice 0 --tx-queue-mem-limit 0 --tx-queue-size 32768 --force-sealing"

## suggestions by tomusdrw in https://github.com/paritytech/parity-ethereum/issues/10382#issuecomment-466373932
PARITY_ARGS="--config dev --geth --gasprice 0 --gas-floor-target=40000000 --jsonrpc-server-threads 8 --jsonrpc-threads=0 --tx-queue-mem-limit 0 --tx-queue-per-sender 8192 --tx-queue-size 32768 --no-discovery --fast-unlock"


PARITY_CONSENSUS=instantseal

# very strange naming for the folder, instead of deployment/1/ this is deployment/is_authority/ 
FIRST_NODE=is_authority

source networks/parity-configure.sh $1