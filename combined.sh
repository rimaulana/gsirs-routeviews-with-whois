#!/bin/bash

SCRIPT=$(readlink -f $0)
ROOTDIR=`dirname $SCRIPT`

resultFiles=($(ls $ROOTDIR/dest/ | grep csv))
totalResultFiles=`ls $ROOTDIR/dest/ | grep csv | wc -l`
counter=1
echo "\"ASN\",\"DATE\",\"RV-ROUTE\",\"RV-LENGTH\",\"WHOIS-ROUTE\",\"WHOIS-LENGTH\",\"AUTHORITIES\",\"CREATED\",\"STATUS\",\"COUNTRY\"" > $ROOTDIR/result.csv
for file in ${resultFiles[@]}
do
    tail -n +2 $ROOTDIR/dest/$file >> $ROOTDIR/result.csv
    if [[ $((counter%10)) -eq 0 ]]; then
        clear
        $ROOTDIR/progress.sh 40 $counter $totalResultFiles
    fi
    ((counter=counter+1))
done
