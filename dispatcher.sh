#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`
maxActiveWorker=8
pingInterval=10
pingTimer=0

echo "$$" > $ROOTDIR/dispatcher.pid
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
    if $Connected; then
        activeWorker=`ps ax -o cmd | grep worker.py | awk '{if($1 == "python"){print $1}}' | wc -l`
        newSpawn=$((maxActiveWorker - activeWorker))
        if [[ $newSpawn -gt 0 ]]; then
            list=($(ls $ROOTDIR/pool/ | head -$newSpawn))
            for file in ${list[@]}
            do
                mv $ROOTDIR/pool/$file $ROOTDIR/worked/$file
                nohup python $ROOTDIR/worker.py $file &
            done
        fi
    fi
    ((pingTimer=pingTimer+1))
done
