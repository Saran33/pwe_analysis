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

class Security:
    def __init__(self, inp):
        if ".csv" in inp:
            self.df = self.eq1(ip);
        else:
            self.df = self.eq2(inp);
            
        if hasattr(self.df, 'name'):   
            self.name = self.df.name
        else:
            raise Exception("Please name the DataFrame first before creating this object. Use df.name = 'Some_Name.'\nUse the ticker or symbol.")
    
            self.stats 
        
    def eq1(self, inp):
        x = pd.read_csv(inp,low_memory=False,index_col=['Date'], parse_dates=['Date']
                        ,infer_datetime_format=True,)
        return x;
    
    def eq2(self, inp):
        y = (inp)
        
        return y;
        
        # Period returns:
    def get_returns(self, returns='Price_Returns',price='Close'):
        """
        Calculate percentage returns.
        """
        df = self.df
        
        df['Price'] = df[price].copy()
        
        #df['Price_Returns'] = (df['Price'] - df['Price'].shift(1))/df['Price'].shift(1)
        df[f'{returns}'] = (df[price] /df[price].shift(1) - 1)
        
        df['Log_Returns'] = np.log(df[price]/df[price].shift(1)).dropna()
        #df['log_ret'] = np.log(df[price]) - np.log(df[price].shift(1))
        # x =  np.around((df1['Log_Returns'] - df1['log_ret']).cumsum(),100)
        
        for row in df.itertuples():
            df['Cumulative Returns'] = (df[price] - df[price].iloc[0]) / df[price].iloc[0]
            
        return;
    
    def vwap(self, h='High',l='Low',c='Close',v='Volume',window=None):
        """
        Volume-Weighted Average Price.
        VWAP = (Cumulative (Price * Volume)) / (Cumulative Volume)
        
        """
        df = self.df
        
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
        Support function for the vwap_close fucntion below:
        """
        return ((df[price]*df[volume]).sum()/df[volume].sum()).round(2);
    
    def vwap_close(self,window=1, price='Close', volume='Volume'):
        """
        Returns the Volume-Weighted Average Price for Close prices or Adj. Close prices.
        """
        df = self.df
        
        vwap = pd.concat([ (pd.Series(vwp(df.iloc[i:i+window],price,volume),
                                   index=[df.index[i+window]])) for i in range(len(df)-window) ]);
        vwap = pd.DataFrame(vwap, columns=['Close_VWAP'])
        df = df.join(vwap, how='left')
        
        return df;
    
    def stats(self, returns='Price_Returns',price='Close', trading_periods=252,market_hours=24,interval='daily', vol_window = 30): 
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
        df = self.df;
        #self.name = f'{df=}'.split('=')[0]
        
        start_date = df.index.min();
        end_date = df.index.max();

        if interval =='daily':
            ann_factor = trading_periods;
            t = 'days';
            #vol_window = vol_window
        elif interval =='annual':
            ann_factor = 1;
            t = 'years';
            #vol_window = vol_window
        elif interval =='hourly':
            ann_factor = trading_periods*market_hours;
            t = 'hours';
            #vol_window = vol_window*market_hours
        elif interval =='minutes':
            ann_factor = trading_periods*market_hours*60;
            t = 'minutes';
            #vol_window = vol_window*market_hours*60
        elif interval =='seconds':
            ann_factor = trading_periods*market_hours*(60**2);
            t = 'seconds';
            #vol_window = vol_window*market_hours*(60**2)
        elif interval =='weekly':
            ann_factor = 52;
            t = 'weeks';
            #vol_window = vol_window/7
        elif interval =='quarterly':
            ann_factor = 4;
            t = 'quarters';
        elif interval =='semiannual':
            ann_factor = 2;
            t = 'half years'
        elif interval =='monthly':
            ann_factor = 12;
            t = 'months';
            print ('')
            
        print ('\n')
        print (f'{self.name} Return stats:')
        print(f"Dates: {start_date} - {end_date}")
        periods = df[returns].count();
        years = periods/ann_factor;
        print (f"Periods: {periods} {t}")
        print (f"Trading Periods: {trading_periods} days a year")
        print("Years: {:.3}".format(years))
        print ('')

        if price in df:
            Security.cum_ret = (df[price].iloc[-1] / df[price].iloc[0])-1;
        else:
            raise ValueError('Include a price index in function paramaterss, e.g. price="Close"')
    
        print ('Cumulative Returns:', "{:.2%}".format(Security.cum_ret))
        print ('')
        
#####################################################################################################################
    
        #Arithmetic average returns:
        Security.avg_ret = df[returns].mean();
        print ('Arithmetic Mean Return:', "{:.6%}".format(Security.avg_ret))
        
        #Geometric average returns:
        Security.geomean = ((1 + Security.cum_ret)**(1/(periods))) - 1
        #Security.geomean = ((1 + Security.cum_ret)**(1/((df[returns].count())*(trading_periods/365.25)))) - 1   #(1/7686) -1  #
        print ('Geometric Mean Return:', "{:.6%}".format(Security.geomean))
        print ('')
        
        #Median returns:
        Security.med_ret = df[returns].median()
        #Security.med_ret = df[returns].round(4).median()
        print ('Median Return:', "{:.6%}".format(Security.med_ret))
        print ('')
        
#####################################################################################################################
        
        #Annualized Return:
        #Security.avg_annualaized = Security.avg_ret * ann_factor
        Security.avg_annualaized = ((1+ Security.avg_ret)**ann_factor)-1
        #Security.avg_annualaized = Security.avg_ret * ann_factor
        print ('Annualaized Arithmetic Return:', "{:.2%}".format(Security.avg_annualaized))
        
        #Annualaized Geometric:
        Security.avg_annualized_geometric = ((1 + Security.cum_ret)**(ann_factor/periods)) - 1
        #Security.avg_annualized_geometric = ((1 + df[returns]).cumprod()) -1
        print ('Annualized Geometric Return:', "{:.2%}".format(Security.avg_annualized_geometric))
        print(' ')
    
#####################################################################################################################
    
        # Volatility of returns:
        Security.std_ret = df['Log_Returns'].std()
        print ('Vol. of Period Returns:', "{:.6%}".format(Security.std_ret))
        
        # Average {vol_window} Day Volatility:
        if f'Vol_{vol_window}' in df:
            Security.vol_roll_mean = df[f'Vol_{vol_window}'].mean()
        else:
            std,an_std,vol_roll,vol_roll_an,vs_vol,r_vol=vol.get_vol(df,window=vol_window,column=returns,trading_periods=ann_factor)
            Security.vol_roll_mean = vol_roll.mean()
        print (f'Mean Volatility ({vol_window}):', "{:.6%}".format(Security.vol_roll_mean))
        
        if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):
            # Average {vol_window} Day YangZhang Estimator:
            yz_roll, yz_roll_an = vol.YangZhang_estimator(df,window=vol_window,trading_periods=trading_periods, clean=True,
                                                              interval=interval,market_hours=market_hours)
            Security.yz_roll_mean = yz_roll.mean()
            print (f'Mean YangZhang ({vol_window}):', "{:.6%}".format(Security.yz_roll_mean))
            print ('')
        else:
            pass
        
        # Annualized Volatility:
        Security.ann_std_ret = Security.std_ret*np.sqrt(ann_factor)
        print ('Annualized Vol:', "{:.2%}".format(Security.ann_std_ret))
        
        # Average Annualized {vol_window} Volatility:
        Security.vol_roll_an = Security.vol_roll_mean*np.sqrt(ann_factor)
        print (f'Annualized Mean Volatility ({vol_window}):', "{:.2%}".format(Security.vol_roll_an))
    
        # Annualized {vol_window} YangZhang:
        if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):        
            Security.yz_roll_an = Security.yz_roll_mean*np.sqrt(ann_factor)
            #yz_yr, yz_yr_an = YangZhang_estimator(df,window=periods,trading_periods=ann_factor,clean=True);
            #Security.yz_yr_an = yz_yr_an.iloc[-1]
            print (f'Annualized Mean YangZhang ({vol_window}):', "{:.2%}".format(Security.yz_roll_an))
            #print (f'Period YangZhang ({periods}):', "{:.2%}".format(Security.yz_yr_an))
        else:
            pass
        print ('')
        
#####################################################################################################################
    
        # Compute Simple Sharpe (No RFR)
        Security.sharpe_ratio_ar = Security.avg_annualaized / (Security.ann_std_ret)
        print ('Arithmetic Sharpe Ratio:', "{:.2f}".format(Security.sharpe_ratio_ar))
        
        # Compute Geometric Sharpe (No RFR)
        Security.sharpe_ratio_geo = Security.avg_annualized_geometric / (Security.ann_std_ret)
        print ('Geometric Sharpe Ratio:', "{:.2f}".format(Security.sharpe_ratio_geo))
        print (' ')
    
#####################################################################################################################
    
        print ('Return Summary Security:')
        
        print(df[returns].describe()) # Pull up summary statistics
        print('######')
        print ('')
            
        return;


    def get_sub_series(self, start_date=None, end_date=None):
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
