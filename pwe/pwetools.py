#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:25:47 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np

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
    elif 'Date' in df:
        df.set_index('Date')
        df['Date'] = df.index.to_series()
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