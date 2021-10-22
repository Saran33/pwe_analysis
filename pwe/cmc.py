#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 12:01:45 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import os
import pandas as pd
from cryptocmd import CmcScraper
from datetime import date, datetime, timedelta
from pwe.pwetools import sort_index, format_ohlc, check_folder, get_str_dates, file_datetime, get_file_datetime, localize_dt_tz, change_tz
import json
import requests


def cmc_data(symbol="BTC", start_date=None, end_date=None):
    """
    Parameters
    ----------
    start_date : TYPE
        DESCRIPTION.
    end_date : TYPE
        DESCRIPTION.
    symbol : TYPE, optional
        DESCRIPTION. The default is "BTC".

    Returns
    -------
    None.

    https://github.com/guptarohit/cryptoCMD/tree/87b80b544c31999313692e4adde7d0055de2c08a

    """

    start_date, end_date = get_str_dates(
        start_date=start_date, end_date=end_date)
    print('')
    print("Security:", symbol)
    print('')

    tkr = symbol.replace('/', '_')

    print("Checking if a file for this ticker with the same start and end dates exists...")

    if os.path.exists(os.path.abspath(f'csv_files/CMC/{tkr}_{start_date}_{end_date}.csv')) == True:
        file_path = os.path.abspath(
            f'csv_files/CMC/{tkr}_{start_date}_{end_date}.csv')

        print("Matching local file exists.")
        print("Reading recent file from CSV...")
        print(file_path)

        df = pd.read_csv(file_path, low_memory=False, index_col=[
                         'Date'], parse_dates=['Date'], infer_datetime_format=True)
        df = sort_index(df)
        df.name = symbol

    else:
        print("No CSV found. Downloading data from API")

        scraper = CmcScraper(symbol, start_date=start_date,
                             end_date=end_date)  # start_date=start_date,

        # get raw data as list of list
        headers, data = scraper.get_data()

        # get data in a json format
        #btc_json_data = scraper.get_data("json")
        # pp(btc_json_data)

        # Pandas dataFrame for the same data
        df = scraper.get_dataframe(date_as_index=True)
        df = sort_index(df)
        df = format_ohlc(df)
        df.name = symbol

        f_name = f'csv_files/CMC/{tkr}_{start_date}_{end_date}.csv'

        check_folder('csv_files/CMC')
        print(f"Saving as csv to: {f_name}")
        #scraper.export("csv", name=f_name)
        df.to_csv(f_name)

    return df


def binance(symbol='BTCUSDT', start_date=None, end_date=None, interval='1h', your_tz="Asia/Dubai"):
    """
    Parameters
    ----------
    start_date : Should be UTC datetime object or a string representing a UTC datetime.
    end_date :   Should be UTC datetime object or a string representing a UTC datetime.
    symbol :     TYPE, optional
                 The default is "BTC".
    your_tz : Your system tz. Binance API does not return klines in UTC. It returns datetimes your local timezone.

    Returns
    -------
    A DataFrame of Binance kline candles with OHLCV prices for a single ticker.  
    """

    #start_date, end_date = get_str_dates(start_date=start_date,end_date=end_date)
    print('')
    print("Security:", symbol)
    print("Interval:", interval)
    print('')

    tkr = symbol.replace('/', '_')

    print("Checking if a file for this ticker with the same start and end dates exists...")
    csv_start, csv_end = get_file_datetime(start_date, end_date)

    file_path = os.path.abspath(
        f'csv_files/Binance/{tkr}_{interval}_{csv_start}_{csv_end}.csv')
    if os.path.exists(file_path) == True:

        print("Matching local file exists.")
        print("Reading recent file from CSV...")
        print(file_path)

        df = pd.read_csv(file_path, low_memory=False, index_col=[
                         'DateTime'], parse_dates=['DateTime'], infer_datetime_format=True)
        df = sort_index(df, utc=False)
        df.name = f"{symbol}_{interval}"

    else:
        print(f"No CSV: {file_path} found. Downloading data from API")

        start_date = localize_dt_tz(start_date, from_tz="UTC", to_tz=your_tz)
        start_date = start_date.replace(tzinfo=None)
        end_date = localize_dt_tz(end_date, from_tz="UTC", to_tz=your_tz)
        end_date = end_date.replace(tzinfo=None)
        last_datetime = start_date
        df_list = []

        while True:
            new_df = get_binance_bars(
                symbol, interval, last_datetime, end_date)
            if new_df is None:
                break
            df_list.append(new_df)
            last_datetime = max(new_df.index) + timedelta(0, 1)

        df = pd.concat(df_list)
        print(df.shape)

        df = change_tz(df, from_tz=your_tz, to_tz="UTC")
        df = sort_index(df)
        df.name = f"{symbol}_{interval}"

        csv_start, csv_end = file_datetime(df)
        f_name = f'csv_files/Binance/{tkr}_{interval}_{csv_start}_{csv_end}.csv'

        check_folder('csv_files/Binance')
        print(f"Saving as csv to: {f_name}")
        df.to_csv(f_name)

    return df


def get_binance_bars(symbol, interval, startTime, endTime):

    url = "https://api.binance.com/api/v3/klines"

    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'

    req_params = {"symbol": symbol, 'interval': interval,
                  'startTime': startTime, 'endTime': endTime, 'limit': limit}

    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))

    if (len(df.index) == 0):
        return None

    df = df.iloc[:, 0:6]
    df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']

    df.Open = df.Open.astype("float")
    df.High = df.High.astype("float")
    df.Low = df.Low.astype("float")
    df.Close = df.Close.astype("float")
    df.Volume = df.Volume.astype("float")

    #df['adj_Close'] = df['Close']

    df.index = [datetime.fromtimestamp(x / 1000.0) for x in df.DateTime]
    df.index.names = ['DateTime']
    df.index = pd.to_datetime(df.index)
    df = df.drop(columns=['DateTime'])

    return df
