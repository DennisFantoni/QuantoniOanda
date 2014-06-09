from time import sleep
#export PYTHONPATH=$PYTHONPATH:/oanda/oandapy
__author__ = 'ubuntu01'

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


import io
import json
import os.path
import math
import argparse
import os

program_name = "Robot Runner"

print(os.environ['PYTHONPATH'].split(os.pathsep))

import oandapy


settings={}

settings_file='settings.json'

argparser=argparse.ArgumentParser(description="run a trade system")
argparser.add_argument('--account',type=int,help='the account number to trade')
argparser.add_argument('--pair',help='the pair to trade (short)')
args=argparser.parse_args()
if os.path.isfile(settings_file):
    with open('settings.json') as data_file:
        settings = json.load(data_file)
else:
    print("no settings file, creating a new one. This one need to have its access_token set correctly!")
    #todo remove below line as it contains secret key
    settings = { "access_token":"cadcxxxxxxxxxxxxxxxxxxxxxxx573ee-d1bxxxxxxxxxxxxxxxxxxxxxxxx1a1f1",
                 "environment":"live"}
    with io.open(settings_file, 'w') as f:
        f.write(unicode(json.dumps(settings)))
        print("written settings file %s",f.name)

print("%s V0.001 started" %program_name)

oanda3_instrument = args.pair     #"USB10Y_USD"
oanda3_accountid = args.account   #475120

#curl -H "Authorization: Bearer cadccca50a597cc271eba795d89573ee-d1b8c0ba147dffb7b639e7f784d1a1f1" https://api-fxpractice.oanda.com/v1/accounts
#oanda = oandapy.API(environment="practice",  access_token=None)
oanda = oandapy.API(environment=settings['environment'], access_token=settings['access_token'])

#tmp=oanda.get_instruments(475120)
response = oanda.get_prices(instruments="EUR_USD")
prices = response.get("prices")
asking_price = prices[0].get("ask")

print("EUR USD is currently %s", asking_price)

sleep_seconds=5

while True:
    #trade oanda3
    sleep(sleep_seconds)
    response = oanda.get_prices(instruments=oanda3_instrument)
    instrument_curprice=response['prices'][0]
    oanda3_curbid=instrument_curprice['bid']
    oanda3_curask=instrument_curprice['ask']
    if 'status' in instrument_curprice:
        oanda3_curstatus=instrument_curprice['status']
    else:
        oanda3_curstatus='live'
    oanda3_curspread=oanda3_curask-oanda3_curbid
    response = oanda.get_account(oanda3_accountid)
    oanda3_NAV=response['balance']+response['unrealizedPl']
    oanda3_margin_used=response['marginUsed']
    oanda3_margin_rate = response['marginRate']  #typically 0.02
    oanda3_margin_rate_inv = 1.0/oanda3_margin_rate  #typically 50
    oanda3_margin_closeout_pct=oanda3_margin_used*oanda3_margin_rate_inv /  oanda3_NAV #need to calculate myself if avail =0
    oanda3_marginAvail=response['marginAvail']  #more precize than calculating it myself
    oanda3_position_size=oanda3_margin_used*oanda3_margin_rate_inv
    ordercomment=""

    if (oanda3_curstatus != "halted"):
        #calculate price for one position
        #assumes acct is in euros
        #assumes instrument is usd/xxx
        #so wont work in many cases
        oanda3_onepos=oanda3_curbid / asking_price   # this is instrument price in usd / EUR USD price
        oanda3_marginneeded_onepos = oanda3_onepos / oanda3_margin_rate_inv

        if (oanda3_marginAvail>oanda3_marginneeded_onepos):
            #calculate excess margin
            #oanda3_excess_margin=(50-oanda3_margin_rate)*50
            #calculate number i can short
            number_to_short=math.floor(oanda3_marginAvail / oanda3_marginneeded_onepos)+0.001
            #short them
            number_to_short=int(number_to_short)
            if number_to_short > 0:
              try:
                  res=oanda.create_order(oanda3_accountid,instrument=oanda3_instrument,units=number_to_short,side="sell",type="market")
                  ordercomment="Sold %04d at %.4f" % (res['tradeOpened']['units'],res['price'])
              except:
                  ordercomment="exception when trying to create order"
              sleep_seconds=1# be quick to follow up after order

        if (oanda3_margin_closeout_pct>90):
            oanda3_margin_reduce_need = (oanda3_margin_used-90)*oanda3_margin_rate_inv
            number_to_go_long = math.floor(oanda3_margin_reduce_need /oanda3_onepos)
            number_to_go_long=int(number_to_go_long)
            res=oanda.create_order(oanda3_accountid,instrument=oanda3_instrument,units=number_to_go_long, side="buy",type="market")
            ordercomment="Bought %s at %s" % (res['units'],res['price'])
            sleep_seconds=1# be quick to follow up after order

        if (oanda3_margin_closeout_pct>65 and oanda3_margin_closeout_pct<75): #be lazy when far from action
            sleep_seconds=10

        if (oanda3_margin_closeout_pct>55 and oanda3_margin_closeout_pct<85): #more alert when closer to action
            sleep_seconds=5

        if (oanda3_margin_closeout_pct<55 or oanda3_margin_closeout_pct>85): #more alert when closer to action
            sleep_seconds=2

        if (oanda3_margin_closeout_pct<51 or oanda3_margin_closeout_pct>89): #more alert when closer to action
            sleep_seconds=1


    print("%.2f %.2f %.2f %.4f %.2f %.2f %.0f %s" % (oanda3_NAV,oanda3_margin_used, oanda3_margin_closeout_pct,oanda3_curspread, oanda3_curbid, oanda3_curask,oanda3_position_size, ordercomment))




print("%s V0.001 ended" %program_name)
