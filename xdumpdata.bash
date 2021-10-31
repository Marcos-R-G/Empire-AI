#!/bin/bash
/usr/citlocal/cs4300/bin/empire << EOF
xdump sect * | ./parse.py
xdump ship * | ./parseShip.py
EOF