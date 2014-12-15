__author__ = 'ubuntu01'

# this script runs continuously and do some housekeeping
# currently the only task is to record and manipulate spread limits

from time import sleep


program_name = "Housekeeper"


import oandapy
import os
import json
# import pprint
import datetime
import robot_api


spreads = robot_api.read_spreads()


settings_file = 'housekeeping.json'
settings = {}

if os.path.isfile(settings_file):
    with open(settings_file) as data_file:
        settings = json.load(data_file)

accesstoken = robot_api.read_account_token()

print("%s V0.001 started" % program_name)

oanda = oandapy.API(environment=settings['environment'], access_token=accesstoken['access_token'])

instruments = oanda.get_instruments(settings[u'account_id'])
#   pprint.pprint(instruments)

for instrument in instruments[u'instruments']:
    instrument_name = instrument[u'instrument']
    if not instrument_name in spreads:
        spreads[instrument_name]=instrument
    else:
        spreads[instrument_name][u'maxTradeUnits']=instrument[u'maxTradeUnits'] # just to show that i can update

def keep_spread_record(spread_record):
    now =datetime.datetime.now()
    then = robot_api.isoparse(spread_record[u'our_timestamp'])
    later = now+datetime.timedelta(days=-7)
    return then>later


getout=False
while not getout:
    for instrument, instrument_dict in spreads.iteritems():
        #  pprint.pprint(instrument_dict)
        instrument_prices = oanda.get_prices(instruments=instrument)
        prices=instrument_prices[u'prices'][0]
        spread = prices[u'ask']-prices[u'bid']
        oanda_timestamp =prices[u'time']
        our_timestamp = datetime.datetime.now().isoformat()
        spread_record = {u'oanda_timestamp':oanda_timestamp,
        u'our_timestamp':our_timestamp,
        u'spread':spread
        }
        if not u'spread_list' in instrument_dict:
            spreads[instrument][u'spread_list']=[]
            spreads[instrument][u'min_spread']=9999999999
            spreads[instrument][u'max_spread']=0
        spreads[instrument][u'spread_list'].append(spread_record)

        # at this point all spreads are updated with new spread lines and every instrument has at least one spread

        # here we should remove spreads older than a week to keep the stats for a week only

    for instrument, instrument_dict in spreads.iteritems():
        spread_list = instrument_dict[u'spread_list']
        max_spread = 0
        min_spread = 9999999999
        new_spread_list =[]
        for spread_record in spread_list:
            cur_spread= spread_record[u'spread']
            if max_spread <cur_spread:
                max_spread  = cur_spread
            if min_spread>cur_spread:
                min_spread=cur_spread
            if keep_spread_record(spread_record):
                new_spread_list.append(spread_record)
        spreads[instrument][u'min_spread']=min_spread
        spreads[instrument][u'max_spread']=max_spread
        spreads[instrument][u'spread_list']=new_spread_list

    robot_api.write_spreads(spreads)

    for instrument, instrument_dict in spreads.iteritems():
        print("{0:10}{1:10}{2:10}".format(instrument,instrument_dict[u'min_spread'],instrument_dict[u'max_spread']))

            # also maintain a stats dict with the lowest and the highest
        # delete old entries (more than 1 week)
        # write out every 15 minutes.
        # then trade system can look up in the stats and use these spreads
        # perhaps also write the individual spreds to a csv file
    sleep(60*15)

