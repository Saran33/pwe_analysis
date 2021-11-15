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


def get_av_ts(symbol, endpoint, start, end, rel_dir, AV_API='ALPHAVANTAGE_API_KEY', interval=None, outputsize='compact'):
    """
    AlphaVatage API
    https://github.com/RomelTorres/alpha_vantage

    endpoint -> intraday, intraday_extended, daily, daily_adjusted, weekly, weekly_adjusted, monthly, monthly_adjusted.timeseries
    outputsize:  The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
    """

    tkr = symbol.replace('/', '_')

    if interval:
        file = f'{rel_dir}/{tkr}_{endpoint}_{interval}_{start}_{end}.csv'
    else:
        file = f'{rel_dir}/{tkr}_{endpoint}_{start}_{end}.csv'
    file_path = os.path.abspath(file)

    print(file_path)

    if os.path.exists(file_path) == True:

        print("Reading recent file from CSV...")
        print(file_path)
        df = pd.read_csv(file_path, low_memory=False, index_col=[
                         'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
        df.name = tkr

    else:
        print("No CSV found. Downloading data from API")
        ts = TimeSeries(key=AV_API, output_format='pandas')  # retries=5
        # Get json object with the intraday data and another with  the call's metadata
        if endpoint == 'intraday':
            df, meta_data = ts.get_intraday(tkr, interval=interval, outputsize=outputsize)
        elif endpoint == 'intraday_extended':
            df, meta_data = ts.get_intraday_extended(tkr, interval=interval, outputsize=outputsize)
        elif endpoint == 'daily':
            df, meta_data = ts.get_daily(tkr, outputsize=outputsize)
        elif endpoint == 'daily_adjusted':
            df, meta_data = ts.get_daily_adjusted(tkr, outputsize=outputsize)
        elif endpoint == 'weekly':
            df, meta_data = ts.get_weekly(tkr)
        elif endpoint == 'weekly_adjusted':
            df, meta_data = ts.get_weekly_adjusted(tkr)
        elif endpoint == 'monthly':
            df, meta_data = ts.get_monthly(tkr)
        elif endpoint == 'monthly_adjusted':
            df, meta_data = ts.get_monthly_adjusted(tkr)
        del_col_num(df)
        sort_index(df)
        df.index.names = ['DateTime']
        df.name = tkr
        if interval:
            f_name = f'{rel_dir}/{tkr}_{endpoint}_{interval}_{start}_{end}.csv'
        else:
            f_name = f'{rel_dir}/{tkr}_{endpoint}_{start}_{end}.csv'
        df.to_csv(f_name)

    return df
