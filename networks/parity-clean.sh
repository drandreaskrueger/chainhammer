#!/bin/bash

FOLDER=networks/repos/paritytech_parity-deploy
GETBACK=../../..
LOG=logs/network.log

cd $FOLDER
docker-compose down -v > $GETBACK/$LOG

echo
echo to remove chains in the data directory, I need sudo access: # TODO: raise issue in parity-deploy
# sudo rm data/?/chains -rf
sudo rm data/*/chains -rf

cd $GETBACK

echo
echo Network cleaned - should start from block 0 again, next time. # | tee -a $GETBACK/$LOG
echo
