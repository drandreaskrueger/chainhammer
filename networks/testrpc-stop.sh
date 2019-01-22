#!/bin/bash
LOG=logs/network.log
PIDFILE=network.pid

echo Stopping PID $(cat $PIDFILE) 

cat $PIDFILE | xargs kill -SIGINT 
echo sleep 2
sleep 2
cat $PIDFILE | xargs kill -9 

rm $PIDFILE

echo
echo Stopped network. 