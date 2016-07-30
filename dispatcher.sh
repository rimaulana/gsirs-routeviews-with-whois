#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`

poolFiles=($(ls $ROOTDIR/pool/))
for file in ${poolFiles[@]}
do
    echo $file
done
