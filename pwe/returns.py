#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 01:58:52 2021

@author: Saran Connolly saran.c@pwecapital.com
"""
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
from . import vol

# This may be used for other metrics relating to volatility:
def get_returns1(df, price='Close'):
    #if df['Open'] in locals() & df['Close'] in locals():
    if 'Open' in df:
        if 'Close' in df:
            df['Price_Returns'] = ((df['Close'] - df['Open'])/df['Open'])
        else:
            df['Price'] = df[price].copy()
            df['Price_Returns'] = (df['Price'] - df['Price'].shift(1))/df['Price']
    else:
        df['Price'] = df[price].copy()
        df['Price_Returns'] = (df['Price'] - df['Price'].shift(1))/df['Price']
    return df['Price_Returns'];

# Period returns:
def get_returns(df, returns='Price_Returns',price='Close'):
    df['Price'] = df[price].copy()
    #df['Price_Returns'] = (df['Price'] - df['Price'].shift(1))/df['Price'].shift(1)
    df[f'{returns}'] = (df[price] /df[price].shift(1) - 1)
    df['Log_Returns'] = np.log(df[price]/df[price].shift(1)).dropna()
    #df['log_ret'] = np.log(df[price]) - np.log(df[price].shift(1))
    # x =  np.around((df1['Log_Returns'] - df1['log_ret']).cumsum(),100)
    return df[returns], df['Log_Returns'];

def vwap(df, h='High',l='Low',c='Close',v='Volume',window=None):
    """
    Volume-Weighted Average Price.
    VWAP = (Cumulative (Price * Volume)) / (Cumulative Volume)
    
    """
    if window == None:
        df['AP'] = (df[[h,l,c]].mean(axis=1))
        # Cumulative price * volume:
        df['CPV'] = (df['AP'] * df[v]).cumsum()
        df['Cum_Volume'] = df[v].cumsum()
        df['VWAP'] = df['CPV']/df['Cum_Volume']
        df.drop(columns=['CPV','Cum_Volume'])
                
    else:
        # Average price:
        df['AP'] = (df[['High','Low','Close']].mean(axis=1))
        # Cumulative price * volume:
        df['CPV'] = (df['AP'] * df[v]).rolling(window, min_periods=1).sum()
        df['Cum_Volume'] = df[v].rolling(window, min_periods=1).sum()
        df['VWAP'] = df['CPV']/df['Cum_Volume']
        df.drop(columns=['CPV','Cum_Volume'])
                
    return;
    
def vwp(df,price,volume): 
    """
    Support function for vwap_close:
    """
    return ((df[price]*df[volume]).sum()/df[volume].sum()).round(2)

def vwap_close(df,window=1, price='Close', volume='Volume'):
    """
    Returns the Volume-Weighted Average Price for Close prices or Adj. Close prices.
    """
    vwap = pd.concat([ (pd.Series(vwp(df.iloc[i:i+window],price,volume),
                               index=[df.index[i+window]])) for i in range(len(df)-window) ]);
    vwap = pd.DataFrame(vwap, columns=['Close_VWAP'])
    df = df.join(vwap, how='left')
    
    return df;

def return_stats(df, returns='Price_Returns',price='Close', trading_periods=252,market_hours=24,interval='daily', vol_window = 30): 
    # price='Close'):
#####################################################################################################################
    """
    returns : A Pandas series of % returns on which to calculate the below statistics.
    
    trading_periods : The number of trading days per year for the given security.
    
    market_hours :  In the case of annualizing intraday returns and volatility, this is a pretty crude calculation.
                Maybe best to keep market_hours at 24, regardless of whether the market is 24 hours each trading day. 
                It's fine for daily candles or higher.
                
    interval: The time interval of the series under examination. 
    Paramaters:(str): 'daily', 'hourly', 'minutes', 'seconds', 'weekly', 'monthly' 'quarterly', 'semiannual', 'annual'
    
    vol_window: The lookback period for calculating volatility estimators.
                For daily intervals or higher, this is multiplied by 1.
                e.g. For a weekly interval, if vol_window=3, this reflects 3 weeks.
                For intraday series, it should be set to the desired number of days. 
                e.g. For an hourly series, the vol_window will be multiplied by the number of trading hours.
    
    """
    stats=pd.DataFrame(index= df.index)
    
    if 'DateTime' in df:
        start_date = df['DateTime'].min()
        end_date = df['DateTime'].max()
    elif 'Date' in df:
        start_date = df['Date'].min()
        end_date = df['Date'].max()
    else:
        df['DateTime'] = df.index.to_series()
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        start_date = df['DateTime'].min()
        end_date = df['DateTime'].max()
        
    if interval =='daily':
        ann_factor = trading_periods
        t = 'days'
        #vol_window = vol_window
    elif interval =='annual':
        ann_factor = 1
        t = 'years'
        #vol_window = vol_window
    elif interval =='hourly':
        ann_factor = trading_periods*market_hours
        t = 'hours'
        #vol_window = vol_window*market_hours
    elif interval =='minutes':
        ann_factor = trading_periods*market_hours*60
        t = 'minutes'
        #vol_window = vol_window*market_hours*60
    elif interval =='seconds':
        ann_factor = trading_periods*market_hours*(60**2)
        t = 'seconds'
        #vol_window = vol_window*market_hours*(60**2)
    elif interval =='weekly':
        ann_factor = 52
        t = 'weeks'
        #vol_window = vol_window/7
    elif interval =='quarterly':
        ann_factor = 4
        t = 'quarters'
    elif interval =='semiannual':
        ann_factor = 2
        t = 'half years'
    elif interval =='monthly':
        ann_factor = 12
        t = 'months'
    
    print ('\n')
    print (f'{df} Return Stats:')
    print(f"Dates: {start_date} - {end_date}")
    periods = df[returns].count()   
    years = periods/ann_factor
    print (f"Periods: {periods} {t}")
    print (f"Trading Periods: {trading_periods} days a year")
    print("Years: {:.3}".format(years))
    print ('')

    for row in df.itertuples():
        df['Cumulative Returns'] = (df[price] - df[price].iloc[0]) / df[price].iloc[0]
    #df['Cumulative Return'])

    if price in df:
        
        # Calculate rolling cumulative P/L:
        # df['Cumulative Returns'] = df[returns].cumsum()
        for row in df.itertuples():
            df['Cumulative Returns'] = (df[price] - df[price].iloc[0]) / df[price].iloc[0]
            
            # Cumulative Return:
            cumulative_returns = (df[price].iloc[-1] / df[price].iloc[0])-1
    else:
        raise ValueError('Include a price index in function paramaterss, e.g. price="Close"')
            
    #stats.cum_ret = ((1 +df['Cumulative Returns'][-t_steps-1]) /1) -1
    stats.cum_ret = cumulative_returns
    print ('Cumulative Returns:', "{:.2%}".format(stats.cum_ret))
    print ('')
    
#####################################################################################################################

    #Arithmetic average returns:
    stats.avg_ret = df[returns].mean()
    print ('Arithmetic Mean Return:', "{:.6%}".format(stats.avg_ret))
    
    #Geometric average returns:
    stats.geomean = ((1 + stats.cum_ret)**(1/(periods))) - 1
    #stats.geomean = ((1 + stats.cum_ret)**(1/((df[returns].count())*(trading_periods/365.25)))) - 1   #(1/7686) -1  #
    print ('Geometric Mean Return:', "{:.6%}".format(stats.geomean))
    print ('')
    
    #Median returns:
    stats.med_ret = df[returns].median()
    #stats.med_ret = df[returns].round(4).median()
    print ('Median Return:', "{:.6%}".format(stats.med_ret))
    print ('')
    
#####################################################################################################################
    
    #Annualized Return:
    #stats.avg_annualaized = stats.avg_ret * ann_factor
    stats.avg_annualaized = ((1+ stats.avg_ret)**ann_factor)-1
    #stats.avg_annualaized = stats.avg_ret * ann_factor
    print ('Annualaized Arithmetic Return:', "{:.2%}".format(stats.avg_annualaized))
    
    #Annualaized Geometric:
    stats.avg_annualized_geometric = ((1 + stats.cum_ret)**(ann_factor/periods)) - 1
    #stats.avg_annualized_geometric = ((1 + df[returns]).cumprod()) -1
    print ('Annualized Geometric Return:', "{:.2%}".format(stats.avg_annualized_geometric))
    print(' ')

#####################################################################################################################

    # Volatility of returns:
    stats.std_ret = df['Log_Returns'].std()
    print ('Vol. of Period Returns:', "{:.6%}".format(stats.std_ret))
    
    # Average {vol_window} Day Volatility:
    if f'Vol_{vol_window}' in df:
        stats.vol_roll_mean = df[f'Vol_{vol_window}'].mean()
    else:
        std,an_std,vol_roll,vol_roll_an,vs_vol,r_vol=vol.get_vol(df,window=vol_window,column=returns,trading_periods=ann_factor)
        stats.vol_roll_mean = vol_roll.mean()
    print (f'Mean Volatility ({vol_window}):', "{:.6%}".format(stats.vol_roll_mean))
    
    if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):
        # Average {vol_window} Day YangZhang Estimator:
        yz_roll, yz_roll_an = vol.YangZhang_estimator(df,window=vol_window,trading_periods=trading_periods, clean=True,
                                                          interval=interval,market_hours=market_hours)
        stats.yz_roll_mean = yz_roll.mean()
        print (f'Mean YangZhang ({vol_window}):', "{:.6%}".format(stats.yz_roll_mean))
        print ('')
    else:
        pass
    
    # Annualized Volatility:
    stats.ann_std_ret = stats.std_ret*np.sqrt(ann_factor)
    print ('Annualized Vol:', "{:.2%}".format(stats.ann_std_ret))
    
    # Average Annualized {vol_window} Volatility:
    stats.vol_roll_an = stats.vol_roll_mean*np.sqrt(ann_factor)
    print (f'Annualized Mean Volatility ({vol_window}):', "{:.2%}".format(stats.vol_roll_an))

    # Annualized {vol_window} YangZhang:
    if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):        
        stats.yz_roll_an = stats.yz_roll_mean*np.sqrt(ann_factor)
        #yz_yr, yz_yr_an = YangZhang_estimator(df,window=periods,trading_periods=ann_factor,clean=True);
        #stats.yz_yr_an = yz_yr_an.iloc[-1]
        print (f'Annualized Mean YangZhang ({vol_window}):', "{:.2%}".format(stats.yz_roll_an))
        #print (f'Period YangZhang ({periods}):', "{:.2%}".format(stats.yz_yr_an))
    else:
        pass
    print ('')
    
#####################################################################################################################

    # Compute Simple Sharpe (No RFR)
    stats.sharpe_ratio_ar = stats.avg_annualaized / (stats.ann_std_ret)
    print ('Arithmetic Sharpe Ratio:', "{:.2f}".format(stats.sharpe_ratio_ar))
    
    # Compute Geometric Sharpe (No RFR)
    stats.sharpe_ratio_geo = stats.avg_annualized_geometric / (stats.ann_std_ret)
    print ('Geometric Sharpe Ratio:', "{:.2f}".format(stats.sharpe_ratio_geo))
    print (' ')

#####################################################################################################################

    print ('Return Summary Stats:')
    
    print(df[returns].describe()) # Pull up summary statistics
    print('######')
    print ('')
    return stats;

def get_sub_series(df, start_date=None, end_date=None):
    """
	df: dataframe to split
	
	start_date: Default DateTime is one year from now in UTC.
	
	end_date: Default DateTime is now in UTC.
    """
    if start_date==None:
        utc_now = datetime.utcnow()
        auto_start = utc_now - timedelta(days=365)
        start_date = auto_start
        
    if end_date==None:
        end_date = datetime.utcnow()
        
    start_date = pd.to_datetime(start_date)     
    end_date = pd.to_datetime(end_date)
        
    df['DateTime'] = pd.DatetimeIndex(df.index)
    df['DateTime'] = pd.to_datetime(df.index)
    subseries_df = df[(df['DateTime']>=start_date)&(df['DateTime']<=end_date)]
    subseries_df.name = f"{start_date}-{end_date}"
    return subseries_df;
