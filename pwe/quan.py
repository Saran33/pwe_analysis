#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:12:43 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import os
import pandas as pd
import quandl
from datetime import datetime,date,timedelta
from pwe.pwetools import sort_index,format_ohlc,check_folder,get_dates

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

def q_get(symbol,start_date=None,end_date=None, key=None):
    
    quandl_api_key = check_quandl_key(key)
    
    df = quandl.get(symbol,api_key=quandl_api_key, start_date=start_date, end_date=end_date)
    
    df = sort_index(df)
    df = format_ohlc(df)
    
    return df;

def quandl_data(symbol,start_date=None,end_date=None,key=None, file=None):
    """
    Read data from Quandl and store it to a CSV. If the data is recent, it will read from csv 
    rather than making an API request.
    
    """
    if (file==None) and (start_date!=None):
        
        start_date, end_date = get_dates(start_date=start_date,end_date=end_date)
        print("Security:", symbol)
    
        tkr = symbol.replace('/', '_')
    
        if os.path.exists(os.path.abspath(f'csv_files/{tkr}_{start_date}_{end_date}.csv')) == True:
            file_path = os.path.abspath(f'csv_files/{tkr}_{start_date}_{end_date}.csv')
        
            print ("Reading recent file from CSV...")
            print(file_path)
        
            df = pd.read_csv(file_path,low_memory=False, index_col=['Date'], parse_dates=['Date'],infer_datetime_format=True)
            df.name = symbol
            
        else:
            print ("No CSV found. Downloading data from API") 

            df = q_get(symbol,start_date,end_date,key)
            df.name = symbol
        
            check_folder('csv_files')
            f_name = f'csv_files/{tkr}_{start_date}_{end_date}.csv'
            print (f"Saving as csv to: {f_name}")
            df.to_csv(f_name)
            
    else:
        file_path = os.path.abspath(file)
        print (file_path)
        print("Security:", symbol)
    
        tkr = symbol.replace('/', '_')
    
        if os.path.exists(file_path) == True:
        
            print ("Reading recent file from CSV...")
            print(file_path)
        
            df = pd.read_csv(file_path,low_memory=False, index_col=['Date'], parse_dates=['Date'],infer_datetime_format=True)
            df.name = symbol

        else:
            print ("No CSV found. Downloading data from API") 

            df = q_get(symbol,start_date,end_date,key)
            df.name = symbol
        
            check_folder('csv_files')
            f_name = f'csv_files/{tkr}_{start_date}_{end_date}.csv'
            print (f"Saving as csv to: {f_name}")
            df.to_csv(f_name)
    
    return df;
    