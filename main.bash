#!/bin/bash
export COUNTRY=62
export PLAYER=62
export EMPIREPORT=2832
export EMPIREHOST=empire.cs.dixie.edu
stop=0
./explore.py
while [ $stop != 1 ]; do
  ./xdumpdata.bash
  ./search.bash
  stop=$?
  ./wait_for_update.bash
done