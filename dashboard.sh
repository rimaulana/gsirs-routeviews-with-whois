#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`

while true
do
    dispatcherPID=`cat $ROOTDIR/dispatcher.pid`
    poolFiles=`ls $ROOTDIR/pool/ | wc -l`
    workedFiles=`ls $ROOTDIR/worked/ | wc -l`
    resultFiles=`ls $ROOTDIR/result/ | wc -l`
    activeWorker=`ps aux | grep worker.py | wc -l`
    totalFiles=$((poolFiles + workedFiles))
    percentage=`awk -v t1="$totalFiles" -v t2="$resultFiles" 'BEGIN{printf "%.0f", t2/t1 * 100}'`
    progress=`awk -v t1="$totalFiles" -v t2="$resultFiles" 'BEGIN{printf "%.0f", t2/t1 * 20}'`
    remainder=$((20 - progress))
    lineProgress=""
    for (( c=0; c<$progress; c++ ))
    do
           lineProgress="$lineProgress="
    done
    for (( c=0; c<$remainder; c++ ))
    do
           lineProgress="$lineProgress "
    done
    clear
    echo -e "Process ID         : \e[93m$$\e[0m"
    if ps -p $dispatcherPID > /dev/null; then
        echo -e "Dispatcher status  : \e[92mRunning [ PID: \e[93m$dispatcherPID \e[92m]\e[0m"
    else
        echo -e "Dispatcher status  : \e[31mStopped\e[0m"
    fi
    echo -e "Total active worker: \e[92m$((activeWorker - 1))\e[0m"
    echo -e "Total worked files : \e[92m$workedFiles\e[0m"
    echo -e "Progress           : \e[92m$resultFiles\e[0m out of \e[93m$totalFiles\e[0m"
    echo -e "                   : \e[92m[\e[93m$lineProgress\e[92m] $percentage%\e[0m"
    sleep 1
done
