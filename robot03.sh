#!/bin/bash
PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
python robotrunner.py --account 475120  --settings settings03.json $1 $2

