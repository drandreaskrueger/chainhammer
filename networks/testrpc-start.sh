#!/bin/bash

## now done in run*.sh scripts:
# SEND_PARAMS="sequential"
# PREFIX=TestRPC-Local 

FOLDER=.
GETBACK=.
LOG=$GETBACK/logs/network.log
PIDFILE=network.pid

cd $FOLDER
source env/bin/activate
unbuffer testrpc-py > $LOG 2>&1 &
PID=$!
cd $GETBACK

echo $PID > $PIDFILE
# cat network.pid | xargs kill -SIGINT

echo Started network, call this command for watching the log file:
echo tail -n 10 -f $LOG