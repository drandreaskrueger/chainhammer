#!/bin/bash

PARITY_ARGS="--config dev --geth --gasprice 0 --tx-queue-mem-limit 0 --tx-queue-size 32768 --force-sealing"
PARITY_CONSENSUS=instantseal

# very strange naming for the folder, instead of deployment/1/ this is deployment/is_authority/ 
FIRST_NODE=is_authority

source networks/parity-configure.sh $1