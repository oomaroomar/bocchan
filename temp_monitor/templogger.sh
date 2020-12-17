#!/bin/bash
while true; do
  temperature=$(sensors | head -15 | tail -1 | sed 's/^Package id 0:  +//;s/°.*//')
  time=$(date +'%d/%m/%y-%T' | sed -E 's/^/\"/;s/$/\"/')
  echo "$time, $temperature"
  sleep 2
done
