#!/bin/bash

FOLDER=networks/repos/blk-io_crux/docker/quorum-crux
GETBACK=../../../../..
LOG=logs/network.log

cd $FOLDER
docker-compose -f docker-compose-local.yaml down -v > $GETBACK/$LOG

cd $GETBACK

echo
echo Network cleaned - should start from block 0 again, next time. # | tee -a $GETBACK/$LOG
echo
