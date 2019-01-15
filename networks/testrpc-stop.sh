#!/bin/bash
LOG=logs/network.log
PIDFILE=network.pid

echo Stopping PID $(cat $PIDFILE) 

cat $PIDFILE | xargs kill -SIGINT 
sleep 1
cat $PIDFILE | xargs kill -9 

rm $PIDFILE

echo
echo Stopped network. 