#!/bin/bash

# PARITY_ARGS="--nodes 4 --config aura --geth --gasprice 0 --tx-queue-mem-limit 0 --tx-queue-size 32768 --force-sealing"

## suggestions by tomusdrw in https://github.com/paritytech/parity-ethereum/issues/10382#issuecomment-466373932
PARITY_ARGS="--nodes 4 --config aura --geth --gasprice 0 --gas-floor-target=40000000 --jsonrpc-server-threads 8 --jsonrpc-threads=0 --tx-queue-mem-limit 0 --tx-queue-per-sender 8192 --tx-queue-size 32768 --no-discovery --fast-unlock --force-sealing"

PARITY_CONSENSUS=aura
FIRST_NODE=1
source networks/parity-configure.sh $1