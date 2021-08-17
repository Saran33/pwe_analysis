#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:07:49 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np

def get_vol(df, window=21, column='Price_Returns', trading_periods=252):
    # 1 month window = 21
    # 3 month window = 63 
    
    # Standard deviation:
    #df['{} Day Ann. Vol'.format(window)]= (df[column].rolling(window,center=False).std())*np.sqrt(trading_periods)
    df['Std_{}'.format(window)] = (df[column].rolling(window).std())
    std = df['Std_{}'.format(window)]
    df['Ann_Std_{}'.format(window)] = (df[column].rolling(window).std())*np.sqrt(trading_periods)
    an_std = df['Ann_Std_{}'.format(window)]
    
    # Volatility of log returns:
    df['Vol_{}'.format(window)] = (df['Log_Returns'].rolling(window).std())
    vol = df['Vol_{}'.format(window)]
    df['Ann_Vol_{}'.format(window)] = (df['Log_Returns'].rolling(window).std())*np.sqrt(trading_periods) 
    an_vol = df['Ann_Vol_{}'.format(window)]
    
    ann_factor = (trading_periods / window)
    #ann_factor = (trading_periods)
    
    # Variance Swaps (returns are not demeaned):
    df['Ann_VS_Var_{}'.format(window)] = np.square(df['Log_Returns']).rolling(window).sum() * ann_factor
    vs_var = df['Ann_VS_Var_{}'.format(window)]
    df['Ann_VS_Vol_{}'.format(window)] = np.sqrt(vs_var)
    vs_vol = df['Ann_VS_Vol_{}'.format(window)]
    
    # Classic by period (returns are demeaned, dof=1)
    df['Realized_Var_{}'.format(window)] = (df['Log_Returns'].rolling(window).var())* ann_factor
    #df['Realized_Var_{}'.format(window)] = (df['Log_Returns'].rolling(window).var())* trading_periods
    r_var = df['Realized_Var_{}'.format(window)]
    df['Realized_Vol_{}'.format(window)] = np.sqrt(r_var)
    r_vol = df['Realized_Vol_{}'.format(window)]
    
    return std,an_std,vol,an_vol,vs_vol,r_vol; #,vs_var,r_var;

"""

### Better Models:
https://github.com/statsmodels/statsmodels

https://github.com/jasonstrimpel/volatility-trading

http://tech.harbourfronts.com/garman-klass-yang-zhang-historical-volatility-calculation-volatility-analysis-python/

"""

import math

def YangZhang_estimator(df, window=6, trading_periods=252, clean=True):
    """
    window : The lookback window for rolling calculation. 
            If series is daily, this is days. If houly, this should be hours.
            e.g. To calculate 30 Day volatility from an hourly series, window should =720,
            if the market is open 24 hours, 7 days a week, 
            or 480 if it is open 24 hours, 5 days per week.
            
    trading_periods : The number of periods in a year. e.g. For a daily series, 252 or 365.
                    For hourly, input the number of trading hours in a year. e.g. 6048 (252*24)
                    
    clean : Whether to drop nan values or not 
            (largely irrelevent for Pandas analysis as nans are dropped automatically)
    """

    log_ho = (df['High'] / df['Open']).apply(np.log)
    log_lo = (df['Low'] / df['Open']).apply(np.log)
    log_co = (df['Close'] / df['Open']).apply(np.log)
    
    log_oc = (df['Open'] / df['Close'].shift(1)).apply(np.log)
    log_oc_sq = log_oc**2
    
    log_cc = (df['Close'] / df['Close'].shift(1)).apply(np.log)
    log_cc_sq = log_cc**2
    
    rs = log_ho * (log_ho - log_co) + log_lo * (log_lo - log_co)
    
    close_vol = log_cc_sq.rolling(window=window,center=False).sum() * (1.0 / (window - 1.0))
    open_vol = log_oc_sq.rolling(window=window,center=False).sum() * (1.0 / (window - 1.0))
    window_rs = rs.rolling(window=window,center=False).sum() * (1.0 / (window - 1.0))

    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    df['YangZhang_{}'.format(window)] = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt)
    yz = df['YangZhang_{}'.format(window)]
    df['YangZhang{}_Ann'.format(window)] = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt) * math.sqrt(trading_periods)
    yz_an = df['YangZhang{}_Ann'.format(window)]

    if clean:
        return yz.dropna(), yz_an.dropna();
    else:
        return yz, yz_an;