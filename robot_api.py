__author__ = 'ubuntu01'


import os
import json
import datetime

def get_spreads_filename():
    return 'spreads2.json'


def get_account_token_filename():
    return 'quantoni_oanda.json'


def write_spreads(spreads):
    with open(get_spreads_filename(), 'w') as f:
        f.write(unicode(json.dumps(spreads)))
    print("written spreads file %s", f.name)

def read_spreads():
    spreads = {}

    spreads_file =get_spreads_filename()

    if os.path.isfile(spreads_file):
        with open(spreads_file , 'r') as data_file:
            spreads = json.load(data_file)
    return spreads


def read_account_token():
    account_token = {}

    account_token_file =get_account_token_filename()

    if os.path.isfile(account_token_file):
        with open(account_token_file, 'r') as data_file:
            account_token = json.load(data_file)
    return account_token

# change isoformat string to a datetime
def isoparse(s):
    return datetime.datetime(
        int(s[0:4]),
        int(s[5:7]),
        int(s[8:10]),
        int(s[11:13]),
        int(s[14:16]),
        int(s[17:19]))