#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 19:34:59 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import os
import pandas as pd
from pwe.pwetools import del_col_num, sort_index, df_to_csv, dt_to_str, check_folder
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies


def get_av_ts(ticker, endpoint, start, end, rel_dir, AV_API='ALPHAVANTAGE_API_KEY', interval=None, outputsize='compact', save_csv=False):
    """
    AlphaVatage API
    https://github.com/RomelTorres/alpha_vantage

    endpoint -> intraday, intraday_extended, daily, daily_adjusted, weekly, weekly_adjusted, monthly, monthly_adjusted.
    interval -> 1min, 5min, 15min, 30min, 60min
    outputsize:  The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
    """

    tkr = ticker.replace('/', '_')

    if endpoint in ['intraday', 'intraday_extended']:
        if interval:
            relpath = f'{rel_dir}/{tkr}_{endpoint}_{interval}_{start}_{end}.csv'
    else:
        relpath = f'{rel_dir}/{tkr}_{endpoint}_{start}_{end}.csv'
    file_path = os.path.abspath(relpath)

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
            df, meta_data = ts.get_intraday(
                tkr, interval=interval, outputsize=outputsize)
        elif endpoint == 'intraday_extended':
            df, meta_data = ts.get_intraday_extended(
                tkr, interval=interval, outputsize=outputsize)
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
        start = df.index.min()
        end = df.index.max()
        if interval:
            relpath = f'{rel_dir}/{tkr}_{endpoint}_{interval}_{start}_{end}.csv'
        else:
            relpath = f'{rel_dir}/{tkr}_{endpoint}_{start}_{end}.csv'
        if save_csv:
            df.to_csv(relpath, index=True)
            abs_path = os.path.abspath(relpath)
            print("Saved data to:", abs_path)

    return df


def av_interval(interval):
    """Convert pwe.charts.calc_interval() interval to a format for the Alpha Vantage API intraday endpoint.
    interval -> seconds, minutes, hourly, 
    Returns -> 1min, 5min, 15min, 30min, 60min
    """
    if interval == 'minutes':
        av_interval = '1min'
    if interval == 'hourly':
        av_interval = '60min'
    elif interval in ['daily', '5min', '15min', '30min', 'seconds', 'weekly', 'monthly', 'semi-annual', 'annual']:
        av_interval = interval
    return av_interval


def get_multi_av_ts(tickers, endpoint, start, end, rel_dir, AV_API='ALPHAVANTAGE_API_KEY', interval=None,
                    outputsize='compact', price='Close', save_csv=False, miss_sec_lst=False):
    """
    AlphaVatage API
    https://github.com/RomelTorres/alpha_vantage
    Pass a list of tickers to Alpha Vantage API (seperate calls), with each concatonated to a combined dataframe,
    with the option of saving each security to an individual csv.

    endpoint -> intraday, intraday_extended, daily, daily_adjusted, weekly, weekly_adjusted, monthly, monthly_adjusted.
    interval -> 1min, 5min, 15min, 30min, 60min
    outputsize:  The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
    
    If miss_sec_lst = True, returns a concatonated dataframe and a list of any missing securities that failed to download.
                            Or else just returns a concatonated dataframe.
    """

    print('')
    # print("Securities:", tickers)
    print('')

    tkrs = []
    for t in tickers:
        tkr = t.replace('/', '_')
        tkrs.append(tkr)

    print("Checking if ticker files exist locally...")
    csv_start = dt_to_str(start)
    csv_end = dt_to_str(end)

    df_list = []
    missing_secs = []
    check_folder(rel_dir)

    for tkr in tkrs:
        if endpoint in ['intraday', 'intraday_extended']:
            if interval:
                relpath = f'{rel_dir}/{tkr}_{endpoint}_{interval}_{start}_{end}.csv'
        else:
            relpath = f'{rel_dir}/{tkr}_{endpoint}_{start}_{end}.csv'
        file_path = os.path.abspath(relpath)
        
        if os.path.exists(file_path) == True:

            print("Matching local file exists.")
            print(file_path)

            df = pd.read_csv(file_path, low_memory=False, index_col=[
                'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
            print(f"Read local CSV for {tkr}")
            # df = sort_index(df, utc=False)
            df = df[[price]]
            df = df.rename(columns={price: tkr})
            # df.name = f"{tkr}"
            df_list.append(df)

        else:
            print(
                f"No CSV for {tkr} found. Downloading data from AlphaVatage API")
            if interval in ['minutes', 'hourly']:
                interval = av_interval(interval)
            df = get_av_ts(tkr, endpoint, start, end, rel_dir, AV_API=AV_API,
                           interval=interval, outputsize=outputsize, save_csv=save_csv)

            if len(df) > 2:
                df = sort_index(df, utc=True)
                df.index.names = ['DateTime']
                print(f"DOWNLOADED: {tkr}")
                print(df[:5])

                df = df[[price]]
                df = df.rename(columns={price: tkr})
                df_list.append(df)
            else:
                print(f"No data found for {tkr}")
                missing_secs.append(tkr)

        # dfs = dfs.join(df)
        if df_list:
            dfs = pd.concat(df_list, axis=1)
        else:
            dfs = pd.DataFrame()

    if miss_sec_lst:
        return dfs, missing_secs
    else:
        return dfs