#!/bin/bash

PARITY_ARGS="--nodes 4 --config aura --geth --gasprice 0 --tx-queue-mem-limit 0 --tx-queue-size 32768 --force-sealing"
PARITY_CONSENSUS=aura
FIRST_NODE=1
source networks/parity-configure.sh $1