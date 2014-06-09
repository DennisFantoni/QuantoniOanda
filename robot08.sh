#!/bin/bash
PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
python robotrunner.py --account 945975 --pair US2000_USD --MCP_buytrigger 10 --MCP_selltrigger 25

