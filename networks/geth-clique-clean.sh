#!/bin/bash

FOLDER=networks/repos/drandreaskrueger_geth-dev
GETBACK=../../..
LOG=logs/network.log

cd $FOLDER
docker-compose down -v > $GETBACK/$LOG
cd $GETBACK

echo
echo Network cleaned - should start from block 0 again, next time. # | tee -a $GETBACK/$LOG
echo