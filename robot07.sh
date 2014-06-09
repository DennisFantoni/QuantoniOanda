#!/bin/bash
PYTHONPATH=${PYTHONPATH}:/home/ubuntu01/IdeaProjects/QuantoniOanda/oanda/oandapy
export PYTHONPATH
python robotrunner.py --account 541631  --pair US2000_USD --MCP_buytrigger 25 --MCP_selltrigger 75

