#!/bin/bash
<<<<<<< HEAD
runtime="3 sec"
=======
runtime="128 sec"
>>>>>>> 809792979164478acd45f2338726ff6aceb01129
endtime=$(date -ud "$runtime" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do
  temperature=$(sensors | head -3 | tail -1 | sed 's/^Package id 0:  +//;s/°.*//')
  time=$(date +'%T' | sed -E 's/^/\"/;s/$/\"/')
  echo "$time, $temperature"
  sleep 1
done
