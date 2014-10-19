__author__ = 'ubuntu01'

# this script runs continously and do some housekeeping
# currently the only task is to record and manipulate spread limits

from time import sleep


program_name = "Housekeeper"


import oandapy
import os
import json


spreads = {}

spreads_file = 'spreads.json'

if os.path.isfile(spreads_file):
    with open(spreads_file) as data_file:
        spreads = json.load(data_file)

settings_file = 'housekeeping.json'
settings = {}

if os.path.isfile(settings_file):
    with open(settings_file) as data_file:
        settings = json.load(data_file)
