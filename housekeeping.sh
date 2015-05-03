#!/bin/bash



PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
for ((;;))
do
    echo python housekeeping.py
    python housekeeping.py
    sleep 10s
done
read -p "finished run_a_robot with parameters $@"