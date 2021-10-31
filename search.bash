#!/bin/bash
python3 search.py > commands.txt
egrep '^(move|distribute|capital|threshold|designate|build|des)' commands.txt > empirecommands.txt
/usr/citlocal/cs4300/bin/empire < empirecommands.txt
if [ -s empirecommands.txt ]; then
  exit 0
else
  exit 1
fi