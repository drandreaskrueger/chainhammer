#!/bin/bash

SEND_PARAMS="threaded2 20"
PREFIX=Quorum-Local # or by CLI parameter?

FOLDER=networks/repos/blk-io_crux/docker/quorum-crux
GETBACK=../../../../..
LOG=logs/network.log
PIDFILE=network.pid

cd $FOLDER
docker-compose -f docker-compose-local.yaml up --build > $GETBACK/$LOG 2>&1 &
PID=$!
cd $GETBACK

echo $PID > $PIDFILE
# cat network.pid | xargs kill -SIGINT

echo
echo For Quorum it can take a minute until the chain starts moving.

echo Started network, call this command for watching the log file:
echo tail -n 10 -f $LOG
echo