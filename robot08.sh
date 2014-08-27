#!/bin/bash
PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
python robotrunner.py --account 945975 --settings settings08.json --MCP_buytrigger 10 --MCP_selltrigger 25 #@

