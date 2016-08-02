#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`

shopt -s extglob
KEY=${1##*( )}
KEY=${KEY%%*( )}
shopt -u extglob

poolFiles=`ls $ROOTDIR/pool/ | wc -l`
workedFiles=`ls $ROOTDIR/worked/ | wc -l`
totalFiles=$((poolFiles + workedFiles))
resultFiles=`ls $ROOTDIR/result/ | wc -l`
percentage=`awk -v t1="$totalFiles" -v t2="$resultFiles" 'BEGIN{printf "%.0f%", t2/t1 * 100}'`

curl -X POST -H "Content-Type: application/json" -d '{"value1":"'$percentage'"}' https://maker.ifttt.com/trigger/gsirs_ping/with/key/$KEY
