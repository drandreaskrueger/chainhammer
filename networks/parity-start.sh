#!/bin/bash

# parity still cannot handle multithreaded sending!
# SEND_PARAMS="threaded2 20"
SEND_PARAMS="sequential"

PREFIX=Parity-Local # or by CLI parameter?

FOLDER=networks/repos/paritytech_parity-deploy
GETBACK=../../..
LOG=logs/network.log
PIDFILE=network.pid

cd $FOLDER
docker-compose up > $GETBACK/$LOG 2>&1 &
PID=$!
cd $GETBACK

echo $PID > $PIDFILE
# cat network.pid | xargs kill -SIGINT

echo Started network, call this command for watching the log file:
echo tail -n 10 -f $LOG
echo