#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 08:33:53 2021

@author: Saran Connolly saran.c@pwecapital.com
"""
from datetime import datetime, date, timedelta
from typing import OrderedDict
import pytz
from os import error
import sys
import pandas as pd
import numpy as np
import math
from pwe.pwetools import first_day_of_current_year, last_day_of_current_year, sort_index, to_utc

from scipy.stats import kurtosis, skew, jarque_bera, shapiro  # anderson,


class Security:
    def __init__(self, inp):
        if ".csv" in inp:
            self.df = self.eq1(inp)
        else:
            self.df = self.eq2(inp)

        if hasattr(self.df, 'name'):
            self.name = self.df.name
        else:
            raise Exception(
                "Please name the DataFrame first before creating this object. Use df.name = 'Some_Name.'\nUse the ticker or symbol.")

        if hasattr(self, 'subseries') == False:
            self.ticker = self.name
        else:
            self.subseries.ticker = None

        self.df.name = self.name
        #self.df._metadata += ['name']

    def eq1(self, inp):
        x = pd.read_csv(inp, low_memory=False, index_col=['Date'], parse_dates=[
                        'Date'], infer_datetime_format=True,)
        return x

    def eq2(self, inp):
        y = (inp)

        return y

        # Period returns:
    def get_returns(self, returns='Price_Returns', price='Close'):
        """
        Calculate percentage returns.
        """
        df = self.df

        df['Price'] = df[price].copy()

        #df['Price_Returns'] = (df['Price'] - df['Price'].shift(1))/df['Price'].shift(1)
        df[f'{returns}'] = (df[price] / df[price].shift(1) - 1)

        df['Log_Returns'] = np.log(df[price]/df[price].shift(1)).dropna()
        #df['log_ret'] = np.log(df[price]) - np.log(df[price].shift(1))
        # x =  np.around((df1['Log_Returns'] - df1['log_ret']).cumsum(),100)

        for row in df.itertuples():
            df['Cumulative Returns'] = (
                df[price] - df[price].iloc[0]) / df[price].iloc[0]

        return

    def vwap(self, h='High', l='Low', c='Close', v='Volume', window=None):
        """
        Volume-Weighted Average Price.
        VWAP = (Cumulative (Price * Volume)) / (Cumulative Volume)

        """
        df = self.df

        if window == None:
            df['AP'] = (df[[h, l, c]].mean(axis=1))
            # Cumulative price * volume:
            df['CPV'] = (df['AP'] * df[v]).cumsum()
            df['Cum_Volume'] = df[v].cumsum()
            df['VWAP'] = df['CPV']/df['Cum_Volume']
            df.drop(columns=['CPV', 'Cum_Volume'])

        else:
            # Average price:
            df['AP'] = (df[[h, l, c]].mean(axis=1))
            # Cumulative price * volume:
            df['CPV'] = (df['AP'] * df[v]).rolling(window, min_periods=1).sum()
            df['Cum_Volume'] = df[v].rolling(window, min_periods=1).sum()
            df['VWAP'] = df['CPV']/df['Cum_Volume']
            df.drop(columns=['CPV', 'Cum_Volume'])

        return

    def vwp(self, price, volume):
        """
        Support function for the vwap_close fucntion below:
        """
        df = self.df

        return ((df[price]*df[volume]).sum()/df[volume].sum()).round(2)

    def vwap_close(self, window=1, price='Close', volume='Volume'):
        """
        Returns the Volume-Weighted Average Price for Close prices or Adj. Close prices.
        """
        df = self.df

        vwap = pd.concat([(pd.Series(self.vwp(df.iloc[i:i+window], price, volume),
                                     index=[df.index[i+window]])) for i in range(len(df)-window)])
        vwap = pd.DataFrame(vwap, columns=['Close_VWAP'])
        df = df.join(vwap, how='left')

        return df

    def get_ann_factor(self, interval, trading_periods, market_hours):

        if interval == 'daily':
            ann_factor = trading_periods
            t = 'days'
            p = 'Day'
            #vol_window = vol_window

        elif interval == 'annual':
            ann_factor = 1
            t = 'years'
            p = "Yr."
            #vol_window = vol_window

        elif interval == 'hourly':
            ann_factor = trading_periods*market_hours
            t = 'hours'
            p = "Hr."
            #vol_window = vol_window*market_hours

        elif interval == 'minutes':
            ann_factor = trading_periods*market_hours*60
            t = 'minutes'
            p = 'Min.'
            #vol_window = vol_window*market_hours*60

        elif interval == 'seconds':
            ann_factor = trading_periods*market_hours*(60**2)
            t = 'seconds'
            p = 'Sec.'
            #vol_window = vol_window*market_hours*(60**2)

        elif interval == 'weekly':
            ann_factor = 52
            t = 'weeks'
            p = 'Wk.'
            #vol_window = vol_window/7

        elif interval == 'quarterly':
            ann_factor = 4
            t = 'quarters'
            p = 'Q.'

        elif interval == 'semiannual':
            ann_factor = 2
            t = 'half years'
            p = 'Six Month'

        elif interval == 'monthly':
            ann_factor = 12
            t = 'months'
            p = 'Month'

        return ann_factor, t, p

    def get_vol(self, window=21, returns='Price_Returns', trading_periods=252, interval='daily',
                market_hours=24):
        """
        1 month window = 21
        3 month window = 63
        window: the lookback period, expressed in terms of the time interval.
        trading_periods : the number of trading days in a year.

        """
        df = self.df

        af, t, p = self.get_ann_factor(interval, trading_periods, market_hours)

        # Standard deviation:
        df['Std_{}_{}'.format(window, p)] = (
            df[returns][1:].rolling(window).std())
        std = df['Std_{}_{}'.format(window, p)]
        df['Ann_Std_{}_{}'.format(window, p)] = (
            df[returns][1:].rolling(window).std())*np.sqrt(af)
        ann_vol = df['Ann_Std_{}_{}'.format(window, p)]

        # Volatility of log returns:
        df['Vol_{}_{}'.format(window, p)] = (
            df['Log_Returns'][1:].rolling(window).std())
        vol = df['Vol_{}_{}'.format(window, p)]
        df['Ann_Vol_{}_{}'.format(window, p)] = (
            df['Log_Returns'][1:].rolling(window).std())*np.sqrt(af)
        an_vol = df['Ann_Vol_{}_{}'.format(window, p)]

        # Variance Swaps (returns are not demeaned):
        df['Ann_VS_Var_{}_{}'.format(window, p)] = np.square(
            df['Log_Returns'][1:]).rolling(window).sum() * af
        vs_var = df['Ann_VS_Var_{}_{}'.format(window, p)]
        df['Ann_VS_Vol_{}_{}'.format(window, p)] = np.sqrt(vs_var)
        vs_vol = df['Ann_VS_Vol_{}_{}'.format(window, p)]

        # Classic by period (returns are demeaned, dof=1)
        df['Realized_Var_{}_{}'.format(window, p)] = (
            df['Log_Returns'][1:].rolling(window).var()) * af
        #df['Realized_Var_{}_{}'.format(window,p)] = (df['Log_Returns'].rolling(window).var())* af
        r_var = df['Realized_Var_{}_{}'.format(window, p)]
        df['Realized_Vol_{}_{}'.format(window, p)] = np.sqrt(r_var)
        r_vol = df['Realized_Vol_{}_{}'.format(window, p)]

        return std, ann_vol, vol, an_vol, vs_vol, r_vol  # ,vs_var,r_var

    def YangZhang_estimator(self, window=6, trading_periods=252, clean=True, interval='daily', market_hours=24):
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
        df = self.df

        af, t, p = self.get_ann_factor(interval, trading_periods, market_hours)

        log_ho = (df['High'] / df['Open']).apply(np.log)
        log_lo = (df['Low'] / df['Open']).apply(np.log)
        log_co = (df['Close'] / df['Open']).apply(np.log)

        log_oc = (df['Open'] / df['Close'].shift(1)).apply(np.log)
        log_oc_sq = log_oc**2

        log_cc = (df['Close'] / df['Close'].shift(1)).apply(np.log)
        log_cc_sq = log_cc**2

        rs = log_ho * (log_ho - log_co) + log_lo * (log_lo - log_co)

        close_vol = log_cc_sq.rolling(
            window=window, center=False).sum() * (1.0 / (window - 1.0))
        open_vol = log_oc_sq.rolling(
            window=window, center=False).sum() * (1.0 / (window - 1.0))
        window_rs = rs.rolling(
            window=window, center=False).sum() * (1.0 / (window - 1.0))

        k = 0.34 / (1.34 + (window + 1) / (window - 1))
        df['YangZhang_{}_{}'.format(window, p)] = (
            open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt)
        yz = df['YangZhang_{}_{}'.format(window, p)]
        df['YangZhang{}_{}_Ann'.format(window, p)] = (
            open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt) * math.sqrt(af)
        yz_an = df['YangZhang{}_{}_Ann'.format(window, p)]

        if clean:
            return yz.dropna(), yz_an.dropna()
        else:
            return yz, yz_an

    def stats(self, returns='Price_Returns', price='Close', trading_periods=252, market_hours=24, interval='daily', vol_window=30, geo=True):
        """
        returns : A Pandas series of % returns on which to calculate the below statistics.

        trading_periods : The number of trading days per year for the given self.

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
        df = self.df
        #self.name = f'{df=}'.split('=')[0]

        start_date = df.index.min()
        end_date = df.index.max()

        if interval == 'daily':
            ann_factor = trading_periods
            t = 'days'
            #vol_window = vol_window
        elif interval == 'annual':
            ann_factor = 1
            t = 'years'
            #vol_window = vol_window
        elif interval == 'hourly':
            ann_factor = trading_periods*market_hours
            t = 'hours'
            #vol_window = vol_window*market_hours
        elif interval == 'minutes':
            ann_factor = trading_periods*market_hours*60
            t = 'minutes'
            #vol_window = vol_window*market_hours*60
        elif interval == 'seconds':
            ann_factor = trading_periods*market_hours*(60**2)
            t = 'seconds'
            #vol_window = vol_window*market_hours*(60**2)
        elif interval == 'weekly':
            ann_factor = 52
            t = 'weeks'
            #vol_window = vol_window/7
        elif interval == 'quarterly':
            ann_factor = 4
            t = 'quarters'
        elif interval == 'semiannual':
            ann_factor = 2
            t = 'half years'
        elif interval == 'monthly':
            ann_factor = 12
            t = 'months'
            print('')

        print('\n')
        if self.ticker == self.name:
            print(f'{self.ticker} Return Stats:')
        else:
            period_str = self.name.replace('_', '', 1)
            print(f'{self.ticker} {period_str} Return Stats:')
        print(f"Dates: {start_date} - {end_date}")
        periods = df[returns].count()
        years = periods/ann_factor
        print(f"Periods: {periods} {t}")
        print(f"Trading Periods: {trading_periods} days a year")
        print("Years: {:.3}".format(years))
        print('')

        if price in df:
            cum_ret = (df[price].iloc[-1] / df[price].iloc[0])-1
            setattr(self, 'cum_ret', cum_ret)
        else:
            raise ValueError(
                'Include a price index in function paramaterss, e.g. price="Close"')

        print('Cumulative Returns:', "{:.2%}".format(self.cum_ret))
        print('')

#####################################################################################################################

        # Arithmetic average returns:
        avg_ret = df[returns].mean()
        setattr(self, 'avg_ret', avg_ret)
        print('Arithmetic Mean Return:', "{:.6%}".format(self.avg_ret))

        # Geometric average returns:
        geomean = ((1 + self.cum_ret)**(1/(periods))) - 1
        setattr(self, 'geomean', geomean)
        #self.geomean = ((1 + self.cum_ret)**(1/((df[returns].count())*(trading_periods/365.25)))) - 1   #(1/7686) -1  #
        print('Geometric Mean Return:', "{:.6%}".format(self.geomean))
        print('')

        # Median returns:
        med_ret = df[returns].median()
        setattr(self, 'med_ret', med_ret)
        #self.med_ret = df[returns].round(4).median()
        print('Median Return:', "{:.6%}".format(self.med_ret))
        print('')

#####################################################################################################################

        # Annualized Return:
        #self.avg_ann = self.avg_ret * ann_factor
        avg_ann = ((1 + self.avg_ret)**ann_factor)-1
        setattr(self, 'avg_ann', avg_ann)
        #self.avg_ann = self.avg_ret * ann_factor
        print('Annualaized Arithmetic Return:', "{:.2%}".format(self.avg_ann))

        if geo:
            # Annualaized Geometric:
            avg_ann_geo = ((1 + self.cum_ret)**(ann_factor/periods)) - 1
            setattr(self, 'avg_ann_geo', avg_ann_geo)
            #self.avg_ann_geo = ((1 + df[returns]).cumprod()) -1
            print('Annualized Geometric Return:',
                  "{:.2%}".format(self.avg_ann_geo))
        print(' ')

#####################################################################################################################

        # Volatility of returns:
        vol = df['Log_Returns'][1:].std()
        setattr(self, 'vol', vol)
        print('Vol. of Period Returns:', "{:.6%}".format(self.vol))

        # Average {vol_window} Day Volatility:
        if f'Vol_{vol_window}' in df:
            self.vol_roll_mean = df[f'Vol_{vol_window}'].mean()
        else:
            std, ann_vol, vol_roll, vol_roll_an, vs_vol, r_vol = self.get_vol(
                window=vol_window, returns=returns, trading_periods=ann_factor)
            vol_roll_mean = vol_roll.mean()
            setattr(self, 'vol_roll_mean', vol_roll_mean)
        print(f'Mean Volatility ({vol_window}):',
              "{:.6%}".format(self.vol_roll_mean))

        if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):
            # Average {vol_window} Day YangZhang Estimator:
            yz_roll, yz_roll_ann = self.YangZhang_estimator(window=vol_window, trading_periods=trading_periods, clean=True,
                                                            interval=interval, market_hours=market_hours)
            yz_roll_mean = yz_roll.mean()
            setattr(self, 'yz_roll_mean', yz_roll_mean)
            print(f'Mean YangZhang ({vol_window}):',
                  "{:.6%}".format(self.yz_roll_mean))
            print('')
        else:
            pass

        # Annualized Volatility:
        ann_vol = self.vol*np.sqrt(ann_factor)
        setattr(self, 'ann_vol', ann_vol)
        print('Annualized Vol:', "{:.2%}".format(self.ann_vol))

        # Average Annualized {vol_window} Volatility:
        vol_roll_an = self.vol_roll_mean*np.sqrt(ann_factor)
        setattr(self, 'vol_roll_an', vol_roll_an)
        print(f'Annualized Mean Volatility ({vol_window}):', "{:.2%}".format(
            self.vol_roll_an))

        # Annualized {vol_window} YangZhang:
        if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):
            yz_roll_ann = self.yz_roll_mean*np.sqrt(ann_factor)
            setattr(self, 'yz_roll_ann', yz_roll_ann)
            #yz_yr, yz_yr_an = YangZhang_estimator(df,window=periods,trading_periods=ann_factor,clean=True);
            #self.yz_yr_an = yz_yr_an.iloc[-1]
            print(f'Annualized Mean YangZhang ({vol_window}):', "{:.2%}".format(
                self.yz_roll_ann))
            #print (f'Period YangZhang ({periods}):', "{:.2%}".format(self.yz_yr_an))
        else:
            pass
        print('')

#####################################################################################################################

        # Compute Simple Sharpe (No RFR)
        sharpe_ar = self.avg_ann / (self.ann_vol)
        setattr(self, 'sharpe_ar', sharpe_ar)
        print('Arithmetic Sharpe Ratio:', "{:.2f}".format(self.sharpe_ar))

        if geo:
            # Compute Geometric Sharpe (No RFR)
            sharpe_geo = self.avg_ann_geo / (self.ann_vol)
            setattr(self, 'sharpe_geo', sharpe_geo)
            print('Geometric Sharpe Ratio:', "{:.2f}".format(self.sharpe_geo))
        print(' ')

#####################################################################################################################

        print('Return Summary self:')

        print(df[returns].describe())  # Pull up summary statistics

        if df[returns].count() >= 5000:
            jarq_bera = jarque_bera(df[returns].dropna())
            setattr(self, 'jarq_bera', jarq_bera)
            print("Jarque-Bera:", jarq_bera)
        elif df[returns].count() < 5000:
            shapiro_wilk = shapiro(df[returns].dropna())
            setattr(self, 'shapiro_wilk', shapiro_wilk)
            print("Shapiro-Wilk :", shapiro_wilk)
        # anderson(df[returns].dropna(), dist='norm')

        kurt = kurtosis(df[returns], nan_policy='omit', fisher=False)
        setattr(self, 'kurt', kurt)
        print("Kurtosis:", kurt)
        skw = skew(df[returns], nan_policy='omit', bias=True)
        setattr(self, 'skw', skw)
        print("Skew:", skw)

        print('######')
        print('')

        return

    def get_sub_series(self, start_date=None, end_date=None, utc=True):
        """
        df: dataframe to split

        start_date: Default DateTime is one year from now in UTC.

        end_date: Default DateTime is now in UTC.
        """
        df = self.df

        if start_date == None:
            utc_now = pytz.utc.localize(datetime.utcnow())
            auto_start = utc_now - timedelta(days=365)
            start_date = auto_start

        if end_date == None:
            end_date = pytz.utc.localize(datetime.utcnow())

        # sd = pd.to_datetime(start_date)
        sd = to_utc(start_date)
        # ed = pd.to_datetime(end_date)
        ed = to_utc(end_date)

        df['DateTime'] = pd.DatetimeIndex(df.index)
        df['DateTime'] = pd.to_datetime(df.index, utc=utc)
        subseries_df = df[(df['DateTime'] >= sd) & (df['DateTime'] <= ed)]
        if ((ed - sd) <= timedelta(days=366)) and (sd.year == ed.year):
            subseries_df.name = f"_{ed.year}"
        else:
            subseries_df.name = f"_{sd.year}_{sd.month}_{sd.day}_{ed.year}_{ed.month}_{ed.day}"

        self.subseries = Security(subseries_df)

        setattr(self, f"{subseries_df.name}", self.subseries)

        #  tkr = self.name.replace('/', '_')
        tkr = self.name
        setattr(self.subseries, 'ticker', tkr)

        print(f"Subseries stored as: {subseries_df.name}")

        return self.subseries

    def get_fibs(self, start=None, end=None, period=None, utc=True):
        """
        Calculate Fibonacci retracement levels, expressed as support and resistance.
        kwargs:
        period :    If None, calculate for the entire DataFrame.
                        If 'ytd', calcualte based on year-to-date high and low.
                        If 'whole', calcualte based on the high and low of entire series.
        start,end : If 'period' not set, alternatively, select a timeframe for highs and lows.
                    The 'period' setting will override start and end.
        If no period, start, or end are provided, the default setting is 'whole.'

        utc :   If True, it will convert all datetimes to UTC.
        """
        from pwe.phi import phi
        df = self.df
        φ = phi(22)
        errors = {}
        while True:
            try:
                if ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):

                    if ((start == None) and (end == None) and (period == None)):
                        period = 'whole'

                    if period == 'whole':

                        range_df = df
                        start_dt = df.index.min()
                        end_dt = df.index.max()

                    elif (period == 'ytd') and (start == None):
                        start_dt = first_day_of_current_year(
                            time=True, utc=utc)
                        end_dt = pd.to_datetime(datetime.now(), utc=utc)

                    elif (period == None) and (start == None):
                        start_dt = df.index.min()
                        start_dt = pd.to_datetime(start_dt, utc=utc)

                    elif (period == None) and (start != None):
                        start_dt = pd.to_datetime(start, utc=utc)

                    elif (period != None) and (start != None):
                        errors[0] = (
                            "\nEnsure that either 'period' or 'start' and 'end' are set, or else neither")
                        errors[1] = (
                            "(if neither, then the high and low of the past year will be used).")
                        raise NotImplementedError

                    if (period == None) and (end == None):
                        end_dt = df.index.max()
                        end_dt = pd.to_datetime(end_dt, utc=utc)

                    elif (period == None) and (end != None):
                        end_dt = pd.to_datetime(end, utc=utc)

                    elif (period != None) and (end != None):
                        errors[0] = (
                            "\nEnsure that either 'period' or 'start' and 'end' are set, or else neither")
                        errors[1] = (
                            "(if neither, then the high and low of the past year will be used).")
                        raise NotImplementedError

                    if (period == None) or (period == 'ytd'):
                        try:
                            range_df = df.loc[(df.index >= start_dt) & (
                                df.index <= end_dt)]
                        except:
                            TypeError
                            print(
                                "\nThere may be a timezone mismatch or other date format issue here.")
                            print(
                                f"Coverting the timezone to UTC. Please verify the times are correct. To check: input: {self.name}.df.head() \n")
                            df.index = pd.to_datetime(df.index, utc=utc)
                            range_df = df.loc[(df.index >= start_dt) & (
                                df.index <= end_dt)]

                    elif period != None:
                        if not (period == 'whole') or (period == 'ytd'):
                            errors[0] = (
                                "\nEnsure that the 'period' setting is correct - either 'whole' or 'ytd'.")
                            errors[1] = (
                                "Alternatively,input start and end dates instead.")
                            raise NotImplementedError

                elif not ('High' in df) and ('Low' in df) and ('Open' in df) and ('Close' in df):
                    errors[0] = (
                        "\nInvalid price data. Please provide OHLC as 'Open','High','Low,'Close'")
                    raise NotImplementedError

                print(f"{start_dt} - {end_dt}\n")

                self.high = np.round(range_df['High'].max(), 2)
                self.low = np.round(range_df['Low'].min(), 2)
                self.f_236 = np.round(
                    self.high-((self.high-self.low)*0.236), 2)
                self.f_382 = np.round(
                    self.high-((self.high-self.low)*(1-(1/φ))), 2)
                self.f_50 = np.round(self.high-((self.high-self.low)*0.5), 2)
                self.f_618 = np.round(
                    self.high-((self.high-self.low)*(1/φ)), 2)

                print(
                    f"high= {self.high}  f_236= {self.f_236}  f_382= {self.f_382}  f_50= {self.f_50}  f_618= {self.f_618}  low= {self.low}")
                return

            except Exception as error:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)
                # print ("Exception object:", exception_object)
                print(error)
                for e in errors.values():
                    if e is not None:
                        print(e)
                break
        return


def to_sec(df, name=None):
    """
    Name a DataFrame and initialize it as a Security instance.
    name :  Default is a string of the df variable name.
    """
    if name == None:
        df.name = f'{df=}'.split('=')[0]
    else:
        df.name = name
    df = Security(df)
    return df


def df_dict_to_sec(df_dict):
    """
    Convert a dict of DataFrames into Security objects.
    df_dict :   a dictionary of DataFrame names as keys and DataFrames as values.

    To unpack all newly created securities within the dict to globals, use: globals().update(dict_of_dfs)
    Or else call the security from within the dict by its key.
    """
    for key in df_dict.keys():
        df_dict[key].name = f"{key}"
        df_dict[key] = Security(df_dict[key])
    return df_dict


def sec_dict_stats(sec_dict, returns='Price_Returns', price='Close', trading_periods=252, market_hours=24, interval='daily', vol_window=30, geo=True):
    """
    Apply the stats function to a dictionary of Securities.
    sec_dict :   a dictionary of pwe Securities.

    To unpack all securities within the dict to globals, use: globals().update(sec_dict)
    Or else call the security from within the dict by its key. i.e. sec_dict[key]
    """
    for key in sec_dict.keys():
        sec_dict[key].stats(returns=returns, price=price, trading_periods=trading_periods,
                            market_hours=market_hours, interval=interval, vol_window=vol_window, geo=geo)
    return sec_dict


def sec_dict_stat(sec_dict, stat):
    """
    Return a stat for each Security in a dict.
    stat (str): 'cum_ret', 'avg_ret', 'geomean', 'med_ret', 'avg_ann', 'avg_ann_geo', 'vol', 'ann_vol', 
                'vol_roll_mean', 'yz_roll_mean', 'yz_roll_ann', 'sharpe_ar', 'sharpe_geo', 
    """
    stat_dict = OrderedDict()
    stat_dict = {key: getattr(sec_dict[key], stat) for key in sec_dict.keys()}
    return stat_dict


def apply_wilcoxon_sr(prefix_strs, group2, returns='Price_Returns',
                      H_1=None, group2_name=None, zero_method='wilcox', correction=False, mode='auto'):
    """
   Apply Wilcoxon SR test to numerous equal lenghth series or compare each series to population median.
   Bit of a hack. Needs to be pasted into a notebook for (eval) to work for python globals.
    """
    from pwe.hyptest import wilcoxon_sr

    for prefix_str in prefix_strs:
        delta_lst = []
        suffix_str_lst = ['_min72_48', '_less48', '_min48_24',
                          '_less24', '_t_min_0', '_plus24', '_plus24_48', '_plus48_72']
        for suffix_str in suffix_str_lst:
            delta_lst.append("{pref}{suff}".format(
                pref=prefix_str, suff=suffix_str))

        delta_dict = OrderedDict()
        for item in delta_lst:
            sec = eval(item)
            if sec.name != item:
                setattr(sec, 'name', item)
            delta_dict[item] = sec

        for key in delta_dict.keys():
            if H_1 == None:
                group1_med = delta_dict[key].df[returns].median()
                group2_med = group2[returns].median()
                if group1_med < group2_med:
                    wilcoxon_sr_p = wilcoxon_sr(delta_dict[key].df[returns], group2[returns], H_1='less', group1_name=key, group2_name=group2_name,
                                                zero_method=zero_method, correction=correction, mode=mode)
                elif group1_med > group2_med:
                    wilcoxon_sr_p = wilcoxon_sr(delta_dict[key].df[returns], group2[returns], H_1='greater', group1_name=key, group2_name=group2_name,
                                                zero_method=zero_method, correction=correction, mode=mode)
                elif group1_med == group2_med:
                    wilcoxon_sr_p = wilcoxon_sr(delta_dict[key].df[returns], group2[returns], H_1='two-sided', group1_name=key, group2_name=group2_name,
                                                zero_method=zero_method, correction=correction, mode=mode)
            elif H_1 != None:
                wilcoxon_sr_p = wilcoxon_sr(delta_dict[key].df[returns], group2[returns], H_1=H_1, group1_name=key, group2_name=group2_name,
                                            zero_method=zero_method, correction=correction, mode=mode)
            setattr(delta_dict[key], 'wilcoxon_sr_p', wilcoxon_sr_p)

    return delta_lst, delta_dict


def apply_man_whitney_u(prefix_strs, group2, returns='Price_Returns',
                        H_1=None, group2_name=None, use_continuity=True, axis=0, method='auto'):
    """
   Recursively apply Mann-Whitney U rank tests to different distributions vs. 1 distribution.
   Bit of a hack. Needs to be pasted into a notebook for (eval) to work for python globals.
    """
    from pwe.hyptest import man_whitney_u

    for prefix_str in prefix_strs:
        delta_lst = []
        suffix_str_lst = ['_min72_48', '_less48', '_min48_24',
                          '_less24', '_t_min_0', '_plus24', '_plus24_48', '_plus48_72']
        for suffix_str in suffix_str_lst:
            delta_lst.append("{pref}{suff}".format(
                pref=prefix_str, suff=suffix_str))

        delta_dict = OrderedDict()
        for item in delta_lst:
            sec = eval(item)
            if sec.name != item:
                setattr(sec, 'name', item)
            delta_dict[item] = sec

        for key in delta_dict.keys():
            if H_1 == None:
                group1_med = delta_dict[key].df[returns].median()
                group2_med = group2[returns].median()
                if group1_med < group2_med:
                    mwu_p = man_whitney_u(delta_dict[key].df[returns], group2[returns], H_1='less', group1_name=key, group2_name=group2_name,
                                          use_continuity=use_continuity, axis=axis, method=method)

                elif group1_med > group2_med:
                    mwu_p = man_whitney_u(delta_dict[key].df[returns], group2[returns], H_1='greater', group1_name=key, group2_name=group2_name,
                                          use_continuity=use_continuity, axis=axis, method=method)

                elif group1_med == group2_med:
                    mwu_p = man_whitney_u(delta_dict[key].df[returns], group2[returns], H_1='two-sided', group1_name=key, group2_name=group2_name,
                                          use_continuity=use_continuity, axis=axis, method=method)
            elif H_1 != None:
                mwu_p = man_whitney_u(delta_dict[key].df[returns], group2[returns], H_1=H_1, group1_name=key, group2_name=group2_name,
                                      use_continuity=use_continuity, axis=axis, method=method)

            setattr(delta_dict[key], 'mwu_p', mwu_p)

    return delta_lst, delta_dict
