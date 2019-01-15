#!/bin/bash

PARITY_ARGS="--config dev --geth --gasprice 0 --tx-queue-mem-limit 0 --tx-queue-size 32768 --force-sealing"
PARITY_CONSENSUS=instantseal
source networks/parity-configure.sh