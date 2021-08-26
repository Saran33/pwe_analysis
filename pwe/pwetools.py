#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:25:47 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
import sys, os
from datetime import date,timedelta
from datetime import datetime,date,timedelta

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
    df.index=pd.DatetimeIndex(df.index)
    
    if 'DateTime' in df:
        df.set_index('DateTime')
        df['Date'] = df.index.to_series().dt.date
        
    elif ('Date' in df) or ('date' in df):
        df.index.names = ['DateTime']
    else:
        pass

    df.sort_index(ascending=True, inplace=True)
    
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
    print (f"Checking if {name} directory exists...")

    if not check_path:
        os.makedirs(name)
        print("Created folder : ", name)
    else:
        print(name, "folder already exists.")
        return name;
    
def file_datetime(df):
    if type(df.index) != 'DatetimeIndex' :
        df.index=pd.DatetimeIndex(df.index)
        
    csv_start = df.index.strftime('%Y-%m-%d_%H:%M:%S').min()
    csv_start = csv_start.strip().replace(':', ',')
        
    csv_end = df.index.strftime('%Y-%m-%d_%H:%M:%S').max()
    csv_end = csv_end.strip().replace(':', ',')
        
    return csv_start, csv_end;
    
def df_to_csv(df,symbol,market=None,interval=None,outputsize=None):
    check_folder('csv_files')

    now_dmymh = str(datetime.now().strftime("%d-%m-%Y_%H,%M"))
    csv_start, csv_end = file_datetime(df)
    
    tkr = symbol.replace('/', '_')
    
    if (market==None) and (interval==None) and (outputsize==None):
        file_path = f'csv_files/{tkr}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    elif (market==None) and (outputsize==None):
        file_path = f'csv_files/{tkr}_{interval}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    elif market==None:
        file_path = f'csv_files/{tkr}_{interval}_{outputsize}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    elif outputsize==None:
        file_path = f'csv_files/{tkr}_{interval}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    else:
        file_path = f'csv_files/{tkr}_{market}_{interval}_{outputsize}_{csv_start}-{csv_end}_asof_{now_dmymh}.csv'
    
    df.to_csv(file_path)
    print (f"Saved csv to {file_path}")
    return;
    
def nan_percent(df):
    nans = df.isnull().sum(axis = 0)
    nan_percent = nans/len(df)
    nan_percent = pd.Series(["{0:.2%}".format(val) for val in nan_percent], index = nan_percent.index) 
    return nan_percent;

def delete_none(_dict):
    """
    Deletes dict keys if their value is None.
    """
    for key, value in list(_dict.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value is None:
            del _dict[key]
        elif isinstance(value, list):
            for v_i in value:
                delete_none(v_i)

    return _dict;

def resample_ohlc(df,interval='1H',o='Open',h='High',l='Low',c='Close',v='Volume',
                  v2=None,msc=None, msc_method='mean'):
    """
    Resamples ohcl data to a different interval.
    interval : The desired interval. default ='1H'
    v2 : An option second volume for some securities expressed in price.
    msc : a miscellaneous column. Specify the name.
    msc_method : How to resample to msc column. Default = mean.
    
    Read the below link to get correct market trading hours when resampling:
    https://atekihcan.com/blog/codeortrading/changing-timeframe-of-ohlc-candlestick-data-in-pandas/
    
    """
    if msc == None:
        msc_method = None
    ohlc = {o: 'first',h: 'max',l: 'min',c: 'last',v: 'sum',v2: 'sum',msc: msc_method}
    ohlc_dict = delete_none(ohlc)
        
    for x in ohlc_dict:
        df = df.resample(interval, offset=0).apply(ohlc_dict) # origin=0
    
    return df;

def blockPrinting(func):
    """
	A decorater used to block function printing to the console.
	
	e.g. : 	# This will not print
			@blockPrinting
			def helloWorld2():
    			print("Hello World!")
			helloWorld2()
	"""
    def func_wrapper(*args, **kwargs):
        # block all printing to the console
        sys.stdout = open(os.devnull, 'w')
        # call the method in question
        value = func(*args, **kwargs)
        # enable all printing to the console
        sys.stdout = sys.__stdout__
        # pass the return value of the method back
        return value

    return func_wrapper;

def to_utc(date):
    date = pd.to_datetime(date,utc=True)
    return date;

def split_datetime(df, day=True,month=True,year=True,time=True):
    if day:
        df['Day'] = df.index.day
    if month:
        df['Month'] = df.index.month
    if year:
        df['Year'] = df.index.year
    if time:
        df['Time'] = df.index.time
    return;

def last_fridays(df):
    split_datetime(df, time=False)
    df['Day'] = df.index.day
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    #df['Time'] = df.index.time
    df['Date'] = pd.to_datetime(df[['Year','Month','Day']])
    #df['DateTime'] = pd.to_datetime(df[['Year','Month','Day','Time']])
    last_fris = pd.DataFrame(df.apply(lambda x: x['Date'] + pd.offsets.LastWeekOfMonth(n=1,weekday=4), axis=1), columns=['Date'])
    #last_fridays = pd.DataFrame(df.apply(lambda x: x['DateTime'] + pd.offsets.LastWeekOfMonth(n=1,weekday=4), axis=1), columns=['DateTime'])
    return last_fris;
