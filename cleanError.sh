#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`

workedList="$ROOTDIR/worked.list"
resultList="$ROOTDIR/result.list"

ls $ROOTDIR/result/ > $resultList
ls $ROOTDIR/worked/ > $workedList

removeFiles=($(diff $resultList $workedList | awk '{print $2}'))
for file in ${removeFiles[@]}
do
    if [[ ! -z "$file" ]]; then
        echo $file
        mv $ROOTDIR/worked/$file $ROOTDIR/pool/$file
    fi
done
rm $resultList
rm $workedList
