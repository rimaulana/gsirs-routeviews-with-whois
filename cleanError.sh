#!/bin/bash

removeFiles=($(diff result/ worked/ | awk '{print $4}'))
for file in ${removeFiles[@]}
do
    mv worked/$file pool/
done
