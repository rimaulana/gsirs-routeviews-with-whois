#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`
pingInterval=10
pingTimer=0

while true
do
    if [[ $((pingTimer)) > $((pingTimer)) ]]; then
        if ping -q -c 1 -W 1 www.google.com >/dev/null; then
            Connected=true
        else
            Connected=false
        fi
        pingTimer=0
    fi
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
    if $Connected; then
        echo -e "Internet status    : \e[92mConnected\e[0m"
    else
        echo -e "Internet status    : \e[91mDisonnected\e[0m"
    fi
    if ps -p $dispatcherPID > /dev/null; then
        echo -e "Dispatcher status  : \e[92mRunning [ PID: \e[93m$dispatcherPID \e[92m]\e[0m"
    else
        echo -e "Dispatcher status  : \e[91mStopped\e[0m"
    fi
    echo -e "Total active worker: \e[96m$((activeWorker - 1))\e[0m"
    echo -e "Progress           : \e[96m$resultFiles\e[0m out of \e[93m$totalFiles\e[0m"
    echo -e "Total worked files : \e[96m$workedFiles\e[0m"
    echo -e ""
    #echo -e "                   : \e[92m[\e[96m$lineProgress\e[92m] \e[96m$percentage\e[92m%\e[0m"
    $ROOTDIR/progress.sh 40 $resultFiles $totalFiles
    #echo -e "[01234567890123456789012345678901234567890]"
    echo -e " "
    echo -e "  \e[92mPID\tELAPSED(s)\tWORKED FILE\e[0m"
    ps ax -o pid,etimes,cmd | grep worker.py | awk '{if($3 == "python"){print "  \033[93m"$1"\t\033[96m"$2"\t\t\033[93m"$5"\033[0m"}}'
    ((pingTimer=pingTimer+1))
    sleep 1
done
