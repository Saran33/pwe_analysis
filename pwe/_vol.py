	#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:07:49 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
import math
from returns import Security


def get_ann_factor(interval,trading_periods,market_hours):
	
    if interval =='daily':
        ann_factor = trading_periods
        t = 'days'
        p = 'Day'
        #vol_window = vol_window
		
    elif interval =='annual':
        ann_factor = 1
        t = 'years'
        p = "Yr."
        #vol_window = vol_window
		
    elif interval =='hourly':
        ann_factor = trading_periods*market_hours
        t = 'hours'
        p = "Hr."
        #vol_window = vol_window*market_hours
		
    elif interval =='minutes':
        ann_factor = trading_periods*market_hours*60
        t = 'minutes'
        p = 'Min.'
        #vol_window = vol_window*market_hours*60
		
    elif interval =='seconds':
        ann_factor = trading_periods*market_hours*(60**2)
        t = 'seconds'
        p = 'Sec.'
        #vol_window = vol_window*market_hours*(60**2)
		
    elif interval =='weekly':
        ann_factor = 52
        t = 'weeks'
        p = 'Wk.'
        #vol_window = vol_window/7
		
    elif interval =='quarterly':
        ann_factor = 4
        t = 'quarters'
        p = 'Q.'
		
    elif interval =='semiannual':
        ann_factor = 2
        t = 'half years'
        p = 'Six Month'
		
    elif interval =='monthly':
        ann_factor = 12
        t = 'months'
        p = 'Month'
    
    return ann_factor, t, p;

def get_vol(df, window=21, column='Price_Returns', trading_periods=252, interval='daily',
            market_hours=24):
    """
    1 month window = 21
    3 month window = 63
    window: the lookback period, expressed in terms of the time interval.
    trading_periods : the number of trading days in a year.
    
    """ 
    af, t, p = get_ann_factor(interval,trading_periods,market_hours)
    
    # Standard deviation:
    df['Std_{}_{}'.format(window,p)] = (df[column].rolling(window).std())
    std = df['Std_{}_{}'.format(window,p)]
    df['Ann_Std_{}_{}'.format(window,p)] = (df[column].rolling(window).std())*np.sqrt(af)
    an_std = df['Ann_Std_{}_{}'.format(window,p)]
    
    # Volatility of log returns:
    df['Vol_{}_{}'.format(window,p)] = (df['Log_Returns'].rolling(window).std())
    vol = df['Vol_{}_{}'.format(window,p)]
    df['Ann_Vol_{}_{}'.format(window,p)] = (df['Log_Returns'].rolling(window).std())*np.sqrt(af) 
    an_vol = df['Ann_Vol_{}_{}'.format(window,p)]
    
    # Variance Swaps (returns are not demeaned):
    df['Ann_VS_Var_{}_{}'.format(window,p)] = np.square(df['Log_Returns']).rolling(window).sum() * af
    vs_var = df['Ann_VS_Var_{}_{}'.format(window,p)]
    df['Ann_VS_Vol_{}_{}'.format(window,p)] = np.sqrt(vs_var)
    vs_vol = df['Ann_VS_Vol_{}_{}'.format(window,p)]
    
    # Classic by period (returns are demeaned, dof=1)
    df['Realized_Var_{}_{}'.format(window,p)] = (df['Log_Returns'].rolling(window).var())* af
    #df['Realized_Var_{}_{}'.format(window,p)] = (df['Log_Returns'].rolling(window).var())* af
    r_var = df['Realized_Var_{}_{}'.format(window,p)]
    df['Realized_Vol_{}_{}'.format(window,p)] = np.sqrt(r_var)
    r_vol = df['Realized_Vol_{}_{}'.format(window,p)]
    
    return std,an_std,vol,an_vol,vs_vol,r_vol; #,vs_var,r_var;

def YangZhang_estimator(df, window=6, trading_periods=252, clean=True, interval='daily',market_hours=24):
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
    
    af, t, p = get_ann_factor(interval,trading_periods,market_hours)

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
    df['YangZhang_{}_{}'.format(window,p)] = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt)
    yz = df['YangZhang_{}_{}'.format(window,p)]
    df['YangZhang{}_{}_Ann'.format(window,p)] = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt) * math.sqrt(af)
    yz_an = df['YangZhang{}_{}_Ann'.format(window,p)]

    if clean:
        return yz.dropna(), yz_an.dropna();
    else:
        return yz, yz_an;