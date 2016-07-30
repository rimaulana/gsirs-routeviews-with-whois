#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`

removeFiles=($(diff $ROOTDIR/result/ $ROOTDIR/worked/ | awk '{print $4}'))
for file in ${removeFiles[@]}
do
    mv $ROOTDIR/worked/$file $ROOTDIR/pool/$file
done
