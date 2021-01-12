#!/bin/bash
runtime="64 sec"
endtime=$(date -ud "$runtime" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do
  temperature=$(sensors | head -15 | tail -1 | sed 's/^Package id 0:  +//;s/°.*//')
  time=$(date +'%T' | sed -E 's/^/\"/;s/$/\"/')
  echo "$time, $temperature"
  sleep 1
done
