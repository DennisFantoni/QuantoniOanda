#!/bin/bash
PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
python robotrunner.py --account 704552 --settings settings05.json

