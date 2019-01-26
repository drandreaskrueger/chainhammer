#!/bin/bash

LOG=logs/network.log
PIDFILE=network.pid
FOLDER=networks/repos/blk-io_crux/docker/quorum-crux
GETBACK=../../../../..

echo Stopping PID $(cat $PIDFILE) first with -SIGINT then with -9 

echo kill with -SIGINT
cat $PIDFILE | xargs kill -SIGINT
echo sleep 14
sleep 14
echo kill with -9
cat $PIDFILE | xargs kill -9
sleep 1

rm $PIDFILE
echo Should be stopped now. 

echo
echo docker-compose down

cd $FOLDER
docker-compose -f docker-compose-local.yaml down &>> $GETBACK/$LOG
cd $GETBACK

echo Done.
echo

echo Reactions should show up in the log file:
echo tail -n 10 $LOG
echo
