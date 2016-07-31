#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`
    
dispatcherPID=`cat $ROOTDIR/dispatcher.pid`
if ps -p $dispatcherPID > /dev/null; then
    echo -e "Dispatcher Run"
    exit
else
    echo -e "Started dispatcher"
    nohup $ROOTDIR/dispatcher.sh &
    #cho -e "Dispatcher status  : \e[31mStopped\e[0m"
fi
