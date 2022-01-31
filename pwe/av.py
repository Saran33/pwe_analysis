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


def get_av_ts(ticker, endpoint, start, end, rel_dir, AV_API='ALPHAVANTAGE_API_KEY', interval=None, outputsize='compact', output_format='pandas', save_csv=False):
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
        ts = TimeSeries(key=AV_API, output_format=output_format)  # retries=5
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



def get_av_crypto(ticker, endpoint, start, end, rel_dir, AV_API='ALPHAVANTAGE_API_KEY', market='USD', interval=None, outputsize='compact', output_format='pandas', save_csv=False):
    """
    AlphaVatage API
    https://github.com/RomelTorres/alpha_vantage

    AV MARKET LIST:::: 

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
        crypto = CryptoCurrencies(key=AV_API, output_format='pandas')  # retries=5
        # Get json object with the intraday data and another with  the call's metadata
        if endpoint == 'intraday':
            df, meta_data = crypto.get_crypto_intraday(
                tkr, market=market, interval=interval, outputsize=outputsize)
        elif endpoint == 'daily':
            df, meta_data = crypto.get_digital_currency_daily(tkr, market=market)
        elif endpoint == 'weekly':
            df, meta_data = crypto.get_digital_currency_weekly(tkr, market=market)
        elif endpoint == 'monthly':
            df, meta_data = crypto.get_digital_currency_monthly(tkr, market=market)
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


def get_av_live(ticker, AV_API='ALPHAVANTAGE_API_KEY', output_format='json'):
    ts = TimeSeries(key=AV_API, output_format=output_format)
    tkr = ticker.replace('/', '')
    if output_format=='json':
        data, meta_data = ts.get_quote_endpoint(tkr)
        return data
    else:
        raise ValueError("get_av_live() function currently only returns a dict. Please update function to return other data types.")


def get_av_live_crypto(from_currency, to_currency='USD', AV_API='ALPHAVANTAGE_API_KEY', output_format='json'):
    crypto = CryptoCurrencies(key=AV_API, output_format=output_format)
    if output_format=='json':
        data, meta_data = crypto.get_digital_currency_exchange_rate(from_currency, to_currency)
        return data
    else:
        raise ValueError("get_av_live_crypto() function currently only returns a dict. Please update function to return other data types.")


def get_crypto_fcas_rating(symbol, AV_API='ALPHAVANTAGE_API_KEY', output_format='json'):
    crypto = CryptoCurrencies(key=AV_API, output_format=output_format)
    symbol = symbol.replace('/', '')
    if output_format=='json':
        data, meta_data = crypto.get_digital_crypto_rating(symbol)
        return data
    else:
        raise ValueError("get_crypto_fcas_rating() function currently only returns a dict. Please update function to return other data types.")


def av_search(keywords, AV_API='ALPHAVANTAGE_API_KEY', output_format='json', best_match=True, cols=[]):
    ts = TimeSeries(key=AV_API, output_format=output_format)
    keywords = str(keywords)
    data, meta_data = ts.get_symbol_search(keywords)
    # data = del_col_num(data)
    data.columns = data.columns.str.strip().str.replace('\d+', '', regex=True).str.replace('.', '', regex=False).str.replace(' ', '')
    if cols:
        data = data[cols]
    if best_match:
        data = data.iloc[0]
    if output_format=='json':
        data = data.to_json(orient='records')
        return data
    elif (output_format == 'pandas') or (output_format == 'df'):
        return data
    else:
        raise ValueError("get_crypto_fcas_rating() function currently only returns a dict or pandas dataframe. Please update function to return other data types.")

# from pprint import pprint as pp
# pp(av_search('BTC', output_format='json', best_match=True, cols=['symbol', 'name']))
# pp(av_search('BTC', output_format='pandas', best_match=False, cols=[]))