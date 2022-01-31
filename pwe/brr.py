'''
# CME Bitcoin Reference rate (BRR) exchanges

https://docs-cfbenchmarks.s3.amazonaws.com/CME+CF+Constituent+Exchanges.pdf

https://www.cfbenchmarks.com/indices/BRTI

https://www.cmegroup.com/content/dam/cmegroup/market-regulation/rule-filings/2021/4/21-155.pdf

### The constituents of the reference index:

- It is the aggregation of executed trade flow of constituent exchanges during a one-hour calculation window (3:00 p.m. to 4:00 p.m. London time).
- All relevant transactions are added to a joint list, recording the trade price and size for each transaction. 
- This one-hour window is then partitioned into twelve, five-minute intervals. 
- For each partition, the volume-weighted median trade price is calculated from the trade prices and sizes of all relevant transactions across all constituent exchanges. 
- The BRR is then derived from the equally-weighted average of the volumeweighted medians of all partitions and published daily at 4:00 p.m. London time.
'''

import os
import warnings
import pandas as pd
from pprint import pprint as pp
from datetime import datetime, date, timedelta, timezone
from pwe.pwetools import del_col_num, sort_index, df_to_csv, dt_to_str, check_folder
from decouple import config
from nomics import Nomics

NOMICS_KEY = config('NOMICS_KEY', default='2018-09-demo-dont-deploy-b69315e440beb145')


today_dmy = date.today().strftime("%d-%m-%Y")

# Exchanges in BRR calc:
# Coinbase is gdax
per1_start = '14-11-2016'
per1_end = '01-04-2017'
per1_constituents = ['bitstamp','gdax','itbit','kraken', 'bitfinex','okcoinusd']

# Exchanges in BRR calc:
per2_start = '14-11-2016'
per2_end = '25-01-2019'
per2_constituents = ['bitstamp','gdax','itbit','kraken',]

per3_start = '26-01-2019'
per3_end = '31-01-2019'
per3_constituents = ['bitstamp','gdax', 'kraken',]

per4_start = '01-02-2019'
per4_end = '29-08-2019'
per4_constituents = ['bitstamp','gdax','itbit','kraken',]

per5_start = '30-08-2019'
per5_end = today_dmy
per5_constituents = ['bitstamp','gdax','itbit','kraken','gemini']

nomics = Nomics("2abc18ac3e2ef507efecb9f7053178820fddc733")

## Period 1
bitstamp,coinbase,itbit,kraken,bitfinex,OKCoin = get_all_exchanges(constituents=per1_constituents)
per1_exchanges = pd.concat([bitstamp,coinbase,itbit,kraken,bitfinex,OKCoin])
pp(per1_exchanges)

bitstamp,coinbase,itbit,kraken = get_all_exchanges(constituents=per2_constituents)
exchanges = pd.concat([bitstamp,coinbase,itbit,kraken])
exchanges



bitstamp_1 = nomics.Candles.get_candles(interval="1d",currency=None,base='BTC',quote='USD',exchange='bitstamp', 
                                        market=None,start=per1_start,end=per1_end, format=None)

pp (bitstamp_1)


import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)