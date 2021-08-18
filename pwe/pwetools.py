#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:25:47 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
import os
from datetime import date,timedelta
import datetime

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

def commas(number):
    return ("{:,}".format(number))

def commas_and_dec(number):
    return ("{:,.2f}".format(number))

def convert_dtype(x):
    if not x:
        return ''
    try:
        return str(x)   
    except:        
        return ''
    
# import numba as nb

def random_array():
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, np.nan]
    out = np.random.choice(choices, size=(1000, 10))
    return out

def loops_fill(arr):
    out = arr.copy()
    for row_idx in range(out.shape[0]):
        for col_idx in range(1, out.shape[1]):
            if np.isnan(out[row_idx, col_idx]):
                out[row_idx, col_idx] = out[row_idx, col_idx - 1]
    return out


    return out

def pandas_fill(arr):
    df = pd.DataFrame(arr)
    df.fillna(method='ffill', axis=1, inplace=True)
    out = df.as_matrix()
    return out

def numpy_fill(arr):
    '''Solution provided by Divakar.'''
    mask = np.isnan(arr)
    idx = np.where(~mask,np.arange(mask.shape[1]),0)
    np.maximum.accumulate(idx,axis=1, out=idx)
    out = arr[np.arange(idx.shape[0])[:,None], idx]
    return out

def rid_na(arr):
    mask = np.isnan(arr)
    idx = np.where(~mask,np.arange(mask.shape[1]),0)
    np.maximum.accumulate(idx,axis=1, out=idx)
    out = arr[np.arange(idx.shape[0])[:,None], idx]
    return out

def sort_index(df):
    if 'DateTime' in df:
        df.set_index('DateTime')
        df['DateTime'] = df.index.to_series()
    elif ('Date' in df) or ('date' in df):
        df.set_index('Date')
        df['Date'] = df.index.to_series()
        df.index.names = ['Date']
    else:
        pass    
    df.index=pd.DatetimeIndex(df.index)
    df.sort_index(ascending=True, inplace=True)
    df['Date'] = df.index.to_series()
    return df;

def format_ohlc(df):
	if 'Close' in df:
		pass
	else:
		df.columns = df.columns.str.strip().str.capitalize().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
	return df;

def del_col_num(df):
	if 'Close' in df:
		pass
	else:
		df.columns = df.columns.str.strip().str.replace('\d+', '').str.replace('.', '').str.replace(' ', '').str.replace('_', '').str.capitalize().str.replace('(', '').str.replace(')', '')
	return df;

def check_folder(name):
    '''
    Check if directory exists, if not, create it
    name : a string for the directory name.
    
    '''
    check_path = os.path.isdir(name)
    print (f"checking if {name} directory exists...")

    if not check_path:
        os.makedirs(name)
        print("created folder : ", name)
    else:
        print(name, "folder already exists.")
        return name;
    
def file_datetime(df):
    if 'DateTime' in df:
        csv_start = df['DateTime'].dt.strftime('%Y-%m-%d_%H:%M:%S').min()
        csv_start = csv_start.strip().replace(':', ',')
        
        csv_end = df['DateTime'].dt.strftime('%Y-%m-%d_%H:%M:%S').max()
        csv_end = csv_end.strip().replace(':', ',')
        
    elif 'Date' in df:  
        csv_start = df['Date'].dt.strftime('%Y-%m-%d_%H:%M:%S').min()
        csv_start = csv_start.strip().replace(':', ',')
        
        csv_end = df['Date'].dt.strftime('%Y-%m-%d_%H:%M:%S').max()
        csv_end = csv_end.strip().replace(':', ',')
        
        return csv_start, csv_end;
    
def df_to_csv(df,symbol,csv_start=None,csv_end=None,today_dmymhs=None,market=None,interval=None,outputsize=None):
    check_folder('csv_files')

    now_dmymh = str(datetime.now().strftime("%d-%m-%Y_%H,%M"))
    csv_start, csv_end = file_datetime(df)
    
    if (market==None) and (interval==None) and (outputsize==None):
        file_path = f'csv_files/{symbol}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    elif (market==None) and (outputsize==None):
        file_path = f'csv_files/{symbol}_{interval}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    elif market==None:
        file_path = f'csv_files/{symbol}_{interval}_{outputsize}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    elif outputsize==None:
        file_path = f'csv_files/{symbol}_{interval}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    else:
        file_path = f'csv_files/{symbol}_{market}_{interval}_{outputsize}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    
    df.to_csv(file_path)
    print (f"Saved csv to {file_path}")
    return;
    
