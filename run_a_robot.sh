#!/bin/bash
PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
for ((;;))
do
    echo -en "\033]0;${2}__${3}\a"
    echo robotrunner.py --account $1 --settings settings_$2.json --MCP_buytrigger $3 --MCP_selltrigger $4 $5 $6
    python robotrunner.py --account $1 --settings settings_$2.json --MCP_buytrigger $3 --MCP_selltrigger $4 $5 $6
    sleep 2s
done
read -p "finished run_a_robot with parameters $@"
