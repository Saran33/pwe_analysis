#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 19:34:59 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import os
import pandas as pd
from pwe.pwetools import del_col_num, sort_index, df_to_csv
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies


def get_av_ts(symbol, interval, start, end, rel_dir, av_api='ALPHAVANTAGE_API_KEY'):
    """
    AlphaVatage API
    https://github.com/RomelTorres/alpha_vantage

    interval -> intraday, intraday_extended, daily_adjusted, daily, monthly_adjusted, monthly, weekly_adjusted, weekly, """

    tkr = symbol.replace('/', '_')

    file = f'{rel_dir}/{tkr}_{interval}_{start}_{end}.csv'
    file_path = os.path.abspath(file)

    print(file_path)

    if os.path.exists(file_path) == True:

        print("Reading recent file from CSV...")
        print(file_path)
        df = pd.read_csv(file_path, low_memory=False, index_col=[
                         'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
        df.name = tkr
        df

    else:
        print("No CSV found. Downloading data from API")
        ts = TimeSeries(key=av_api, output_format='pandas')  # retries=5
        # Get json object with the intraday data and another with  the call's metadata
        df, meta_data = ts.get_monthly_adjusted(tkr)
        del_col_num(df)
        sort_index(df)
        df.index.names = ['DateTime']
        df.name = tkr
        f_name = f"{tkr}_{interval}_{df.index.min()}_{df.index.max()}"
        df.to_csv(f_name)

        return df
