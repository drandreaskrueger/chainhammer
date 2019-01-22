#!/bin/bash

LOG=logs/network.log
PIDFILE=network.pid

echo Stopping PID $(cat $PIDFILE)

cat $PIDFILE | xargs kill -SIGINT
echo sleep 5
sleep 5
cat $PIDFILE | xargs kill -9

rm $PIDFILE

echo
echo Stopped. Reaction added to the tail of the log file, see yourself:
echo tail -n 10 $LOG
echo

