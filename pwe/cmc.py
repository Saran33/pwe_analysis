#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 12:01:45 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import os
import pandas as pd
from cryptocmd import CmcScraper
from datetime import date,timedelta
from pwe.pwetools import sort_index,format_ohlc,check_folder

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

def cmc_data(symbol="BTC",start_date=None,end_date=None):
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
    
    start_date, end_date = get_dates(start_date=start_date,end_date=end_date)
    print('')
    print("Security:", symbol)
    print('')
    
    tkr = symbol.replace('/', '_')

    print ("Checking if a file for this ticker with the same start and end dates exists...")
    
    if os.path.exists(os.path.abspath(f'csv_files/{tkr}_{start_date}_{end_date}.csv')) == True:
        file_path = os.path.abspath(f'csv_files/{tkr}_{start_date}_{end_date}.csv')
        
        print ("Matching local file exists.")
        print ("Reading recent file from CSV...")
        print(file_path)
        
        df = pd.read_csv(file_path,low_memory=False, index_col=['Date'], parse_dates=['Date'],infer_datetime_format=True)
        df= sort_index(df)
        df.name = symbol
        
    else:
        print ("No CSV found. Downloading data from API") 

        scraper = CmcScraper(symbol,start_date=start_date, end_date=end_date) # start_date=start_date,
    
        # get raw data as list of list
        headers, data = scraper.get_data()
    
        # get data in a json format
        #btc_json_data = scraper.get_data("json")
        # pp(btc_json_data)
    
        # Pandas dataFrame for the same data
        df = scraper.get_dataframe(date_as_index=True)
        df= sort_index(df)
        df = format_ohlc(df)
        df.name = symbol
        
        f_name = f'csv_files/{tkr}_{start_date}_{end_date}.csv'
        
        check_folder('csv_files')
        print (f"Saving as csv to: {f_name}")
        #scraper.export("csv", name=f_name)
        df.to_csv(f_name)
    
    return df;
    
    