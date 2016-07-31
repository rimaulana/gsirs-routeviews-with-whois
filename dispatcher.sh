#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`
maxActiveWorker=8

echo "$$" > $ROOTDIR/dispatcher.pid
while true
do
    if ping -q -c 1 -W 1 www.google.com >/dev/null; then
        Connected=true
    else
        Connected=false
    fi
    if $Connected; then
        poolCount=`ls $ROOTDIR/pool/ | wc -l`
        if [[ $((poolCount)) > 0 ]]; then
            activeWorker=`ps aux | grep worker.py | wc -l`
            newSpawn=$((maxActiveWorker - activeWorker + 1))
            poolFiles=($(ls $ROOTDIR/pool/))
            for file in ${poolFiles[@]}
            do
                if [[ $((newSpawn)) > 0 ]]; then
                    mv $ROOTDIR/pool/$file $ROOTDIR/worked/$file
                    nohup python $ROOTDIR/worker.py $file &
                    newSpawn=$((newSpawn - 1))
                fi
            done
        fi
    fi
    sleep 2
done
