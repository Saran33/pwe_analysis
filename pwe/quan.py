#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:12:43 2021

@author: zenman618
"""

import os
import pandas as pd
import quandl
from datetime import datetime,date,timedelta
from . import pwetools
from pwetools import sort_index,format_ohlc

def get_dates(start_date=None,end_date=None):
    # utc_now = datetime.utcnow()
    today = date.today()
    td = today.strftime("%d-%m-%Y")
    today_dmy = str(td)
    if end_date is None:
        end_date = today_dmy
    else:
        pass
    if start_date is None:
        start_date = today - timedelta(days=365)
        start_date = start_date.strftime("%d-%m-%Y")
        start_date = str(start_date)
    else:
        pass
    
    print("Today's date:", today_dmy)
    print(" ")
    print("Start date:", start_date)
    print("End date:", end_date)
    return start_date, end_date;

def create_quandl_key(key):
    cwd = os.getcwd()
    quandl_api_key = quandl.ApiConfig.api_key = key
    quandl.save_key("quandl_api_key", filename="quandl_api_key")
    print(os.path.join(os.path.expanduser('~')))
    quandl_api_key = quandl.save_key(key, filename=f"{cwd}/quandl_api_key")
    print(quandl.ApiConfig.api_key)
    print(quandl_api_key)
    return quandl_api_key;

def check_quandl_key(key=None):
    cwd = os.getcwd()
    if os.path.exists(os.path.abspath(f"{cwd}/quandl_api_key")) == True:
        quandl.read_key(filename="quandl_api_key")
        quandl_api_key = quandl.ApiConfig.api_key
    else:
        quandl_api_key = create_quandl_key(key)
        
        return quandl_api_key;

def q_get(ticker,start_date=None,end_date=None, key=None):
    
    quandl_api_key = check_quandl_key(key)
    
    df = quandl.get(ticker,api_key=quandl_api_key, start_date=start_date, end_date=end_date)
    
    df = sort_index(df)
    df = format_ohlc(df)
    
    return df;

def quandl_data(ticker,start_date=None,end_date=None,key=None):
    """
    Read data from Quandl and store it to a CSV. If the data is recent, it will read from csv 
    rather than making an API request.
    
    """
    
    start_date, end_date = get_dates(start_date=start_date,end_date=end_date)
    print("Security:", ticker)
    
    tkr = ticker.replace('/', '_')
    
    if os.path.exists(os.path.abspath(f'csv_files/{tkr}_{start_date}_{end_date}.csv')) == True:
        file_path = os.path.abspath(f'csv_files/{tkr}_{start_date}_{end_date}.csv')
        
        print ("Reading recent file from CSV...")
        print(file_path)
        
        df = pd.read_csv(file_path,low_memory=False, index_col=['Date'], parse_dates=['Date'],infer_datetime_format=True)
            
    else:
        print ("No CSV found. Downloading data from API") 

        df = q_get(ticker,start_date,end_date,key)
        
        f_name = f'csv_files/{tkr}_{start_date}_{end_date}.csv'
        print (f"Saving as csv to: {f_name}")
        df.to_csv(f_name)
    
    return df;
    