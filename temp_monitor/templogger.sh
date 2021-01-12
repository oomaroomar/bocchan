#!/bin/bash
runtime="128 sec"
endtime=$(date -ud "$runtime" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do
  temperature=$(sensors | head -3 | tail -1 | sed 's/^Package id 0:  +//;s/°.*//')
  time=$(date +'%T' | sed -E 's/^/\"/;s/$/\"/')
  echo "$time, $temperature"
  sleep 1
done
