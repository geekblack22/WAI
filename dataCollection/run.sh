#!/usr/bin/sh

./pp.sh
python3.9 main.py &
echo $!
