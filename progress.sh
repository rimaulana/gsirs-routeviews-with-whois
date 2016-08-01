#!/bin/bash

shopt -s extglob
BarLength=${1##*( )}
BarLength=${BarLength%%*( )}
CurrentProgress=${2##*( )}
CurrentProgress=${CurrentProgress%%*( )}
TotalProgress=${3##*( )}
TotalProgress=${TotalProgress%%*( )}
shopt -u extglob

ProgressBar=`awk -v t1="$TotalProgress" -v t2="$CurrentProgress" -v bl="$BarLength" 'BEGIN{printf "%.0f", t2/t1 * bl}'`
MiddleBar=`awk -v bl="$BarLength" 'BEGIN{printf "%.0f", bl/2-2}'`
Remainder=$(($BarLength-$MiddleBar-4))
percentage=`awk -v t1="$TotalProgress" -v t2="$CurrentProgress" 'BEGIN{printf "%.0f", t2/t1 * 100}'`
PercentageStr="$percentage"
for (( i=${#percentage}; i<3; i++))
do
    PercentageStr=" $PercentageStr"
done
PercentageStr="\e[96m$PercentageStr\e[0m"
counter=0
FinalBar="\e[93m[\e[92m"
while [ $counter -lt $BarLength ]
do
    if [ $counter -eq $MiddleBar ]; then
        FinalBar="$FinalBar$PercentageStr\e[96m%\e[92m"
        ((counter=counter+3))
    fi
    if [ $counter -lt $ProgressBar ]; then
        FinalBar="$FinalBar="
    else
        FinalBar="$FinalBar "
    fi
    ((counter=counter+1))
done 
FinalBar="$FinalBar\e[93m]\e[0m"
echo -e "$FinalBar"
