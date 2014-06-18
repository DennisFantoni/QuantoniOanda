from time import sleep
# export PYTHONPATH=$PYTHONPATH:/oanda/oandapy
__author__ = 'ubuntu01'

#todo code cleanup, change variable away from oanda3 as we run any acct. also check comments
#todo set up spread awarenes, so we don't do trades if spread is too much
#todo change trades so they come with a range that we will accept
#todo create robot05.sh
#todo move money from robot03 to robot05
#todo log info in a logfile
#todo support for other leverage limits than 50 and 90
#todo log important info in another logfile
#todo start up a stock shorting robot with as little money as possible - perhaps a few different leverage profiles
#todo (big task) implement correct s2 trading
#todo take profit module (might need to transfer money, probably not available in api)
#todo if logstring is not different then dont print it
#todo also print the time gotten from the srv
#todo put in sanity checks that for instance blocks trading more than N orders each hour
#todo test a gold like scenario with lowered margin (alternatively buying and selling bc we go off limits)


import io
import json
import os.path
import math
import argparse
import os
import datetime

program_name = "Robot Runner"

print(os.environ['PYTHONPATH'].split(os.pathsep))

import oandapy


settings = {}

settings_file = 'settings.json'

argparser = argparse.ArgumentParser(description="run a trade system")
argparser.add_argument('--account', type=int, help='the account number to trade')
argparser.add_argument('--pair', help='the pair to trade (short)')
argparser.add_argument('--maxpos', type=int, default=999999999999, help='the max. number of units to own in this pair')
argparser.add_argument('--MCP_buytrigger', type=int, default=50,
                       help='MCP below this level triggers buy action up to this level')
argparser.add_argument('--MCP_selltrigger', type=int, default=90,
                       help='MCP below this level triggers sell action down to this level')
args = argparser.parse_args()
if os.path.isfile(settings_file):
    with open('settings.json') as data_file:
        settings = json.load(data_file)
else:
    print("no settings file, creating a new one. This one need to have its access_token set correctly!")
    #todo remove below line as it contains secret key
    settings = {"access_token": "cadcxxxxxxxxxxxxxxxxxxxxxxx573ee-d1bxxxxxxxxxxxxxxxxxxxxxxxx1a1f1",
                "environment": "live"}
    with io.open(settings_file, 'w') as f:
        f.write(unicode(json.dumps(settings)))
        print("written settings file %s", f.name)

print("%s V0.001 started" % program_name)

robot_instrument = args.pair  #"USB10Y_USD"
robot_accountid = args.account  #475120
robot_mcpbuytrigger = args.MCP_buytrigger  # 50
robot_mcpselltrigger = args.MCP_selltrigger  #90
robot_maxpos = args.maxpos

#curl -H "Authorization: Bearer cadccca50a597cc271eba795d89573ee-d1b8c0ba147dffb7b639e7f784d1a1f1" https://api-fxpractice.oanda.com/v1/accounts
#oanda = oandapy.API(environment="practice",  access_token=None)
oanda = oandapy.API(environment=settings['environment'], access_token=settings['access_token'])

tmp = oanda.get_instruments(475120)
response = oanda.get_prices(instruments="EUR_USD")
prices = response.get("prices")
asking_price = prices[0].get("ask")

print("EUR USD is currently %s", asking_price)

sleep_seconds = 1
last_robot_NAV = 0

while True:
    #trade oanda3
    sleep(sleep_seconds)
    try:
        response = oanda.get_prices(instruments=robot_instrument)
        instrument_curprice = response['prices'][0]
        robot_curbid = instrument_curprice['bid']
        robot_curask = instrument_curprice['ask']
        if 'status' in instrument_curprice:
            robot_curstatus = instrument_curprice['status']
        else:
            robot_curstatus = 'live'
        robot_curspread = robot_curask - robot_curbid
        response = oanda.get_account(robot_accountid)
        robot_NAV = response['balance'] + response['unrealizedPl']
        robot_margin_used = response['marginUsed']
        robot_margin_rate = response['marginRate']  #typically 0.02
        robot_margin_rate_inv = 1.0 / robot_margin_rate  #typically 50
        robot_margin_closeout_pct = robot_margin_used * robot_margin_rate_inv / robot_NAV  #need to calculate myself if avail =0
        robot_marginAvail = response['marginAvail']  #more precize than calculating it myself
        robot_position_size = robot_margin_used * robot_margin_rate_inv
        ordercomment = ""

        if (robot_curstatus != "halted"):
            #calculate price for one position
            #assumes acct is in euros
            #assumes instrument is usd/xxx
            #so wont work in many cases
            robot_onepos = robot_curbid / asking_price  # this is instrument price in usd / EUR USD price
            robot_marginneeded_onepos = robot_onepos / robot_mcpbuytrigger  #so if we gear 10 times we need 1/10 margin

            if (robot_margin_closeout_pct < robot_mcpbuytrigger):
                if (robot_marginAvail > robot_marginneeded_onepos):
                    #calculate excess margin
                    #robot_excess_margin=(50-robot_margin_rate)*50
                    #calculate number i can short
                    number_to_short = math.floor(robot_marginAvail / robot_marginneeded_onepos) + 0.001

                    #query the position , how many do we have?
                    #if needed , reduce order so that we do not get above maxpos
                    #short them
                    number_to_short = int(number_to_short)
                    if number_to_short > 0:
                        try:
                            res = oanda.create_order(robot_accountid, instrument=robot_instrument,
                                                     units=number_to_short, side="sell", type="market")
                            ordercomment = "Sold %04d at %.4f" % (res['tradeOpened']['units'], res['price'])
                        except:
                            ordercomment = "exception when trying to create order"
                        sleep_seconds = 1  # be quick to follow up after order

            if (robot_margin_closeout_pct > robot_mcpselltrigger):
                robot_target_margin_used = robot_mcpselltrigger * robot_NAV  #please test
                robot_margin_reduce_need = (robot_margin_used * robot_margin_rate_inv - robot_target_margin_used)
                number_to_go_long = math.floor(robot_margin_reduce_need / robot_onepos)
                number_to_go_long = int(number_to_go_long) + 1  #+1 to get decidedly below max
                number_to_go_long = int(number_to_go_long) + 1  #+1 to get decidedly below max
                if number_to_go_long > 0:
                    try:
                        res = oanda.create_order(robot_accountid, instrument=robot_instrument, units=number_to_go_long,
                                                 side="buy", type="market")
                        ordercomment = "Bought %s at %s" % (res['tradeReduced']['units'], res['price'])
                    except Exception as e:
                        ordercomment = "exception when trying to create sell order(%s)" % str(e)
                    sleep_seconds = 1  # be quick to follow up after order

        #be more alert if we are close to a trigger
        sleep_seconds = max(1, min(robot_margin_closeout_pct - robot_mcpbuytrigger,
                                   robot_mcpselltrigger - robot_margin_closeout_pct))
    except Exception as e:
        ordercomment = "%s - exception occoured (%s)" % (ordercomment, str(e))

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if abs(last_robot_NAV - robot_NAV) > 1 or ordercomment <> "":
        print("%.2f %.2f %.2f %.4f %.2f %.2f %.0f %s %s" % (
            robot_NAV, robot_margin_closeout_pct, robot_margin_used, robot_curspread, robot_curbid, robot_curask,
            robot_position_size, ordercomment,ts))
    last_robot_NAV = robot_NAV

print("%s V0.001 ended" % program_name)
