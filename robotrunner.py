__author__ = 'ubuntu01'

import oandapy
import io
import json
import os.path
program_name = "Robot Runner"

settings={}

settings_file='settings.json'

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

#curl -H "Authorization: Bearer cadccca50a597cc271eba795d89573ee-d1b8c0ba147dffb7b639e7f784d1a1f1" https://api-fxpractice.oanda.com/v1/accounts
#oanda = oandapy.API(environment="practice",  access_token=None)
oanda = oandapy.API(environment=settings['environment'], access_token=settings['access_token'])

response = oanda.get_prices(instruments="EUR_USD")
prices = response.get("prices")
asking_price = prices[0].get("ask")

print("EUR USD is currently %s", asking_price)
print("%s V0.001 ended" %program_name)
