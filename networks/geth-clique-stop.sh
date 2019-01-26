#!/bin/bash

LOG=logs/network.log
PIDFILE=network.pid
FOLDER=networks/repos/drandreaskrueger_geth-dev
GETBACK=../../..

echo Stopping PID $(cat $PIDFILE) first with -SIGINT then with -9 

cat $PIDFILE | xargs kill -SIGINT
echo sleep 5
sleep 5
cat $PIDFILE | xargs kill -9

rm $PIDFILE
echo Should be stopped now. 

echo
echo docker-compose down
cd $FOLDER
docker-compose down &>> $GETBACK/$LOG
cd $GETBACK

echo Done.
echo

echo Reactions should show up in the log file:
echo tail -n 10 $LOG
echo
