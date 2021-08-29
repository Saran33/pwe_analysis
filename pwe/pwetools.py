#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:25:47 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
import sys, os
from pandas.core.frame import DataFrame
import pytz
from datetime import date,timedelta
from datetime import datetime,date,timedelta
import re
import glob

def daterange(start_dt, end_dt):
    dates = []
    for d in range(int ((end_dt - start_dt).days)+1):
        dates.append(start_dt + timedelta(d))
    return dates;

def daterange_str(start_dt, end_dt):
    dates = []
    for d in range(int ((end_dt - start_dt).days)+1):
        dates.append((start_dt + timedelta(d)).strftime("%Y-%m-%d"))
    return dates;

def to_csv(df, f_name, folder='csv_files'):

    check_folder(folder)
    df.to_csv(f_name)

    f_path = os.path.abspath(f_name)

    print (f"saved csv to {f_path}")
    return f_path;

def check_for_recent(dir='csv_files',file_type='csv', horizon='today'):
    """
    Check a directory for a file matching todays's date or the current datetime
    Arguments:
    dir         :   The local directory to check. Default is csv_files.
    file_type   :   The file extension. Default is csv.
    horizon     :   What is to be accepted as a recent file. 
                    Default='today' returns a local file if it matches today's date.
                    'now' will reject a local file if does not match the current datetime.
                    'yesterday' will accept a file from yesterday.
                    'week' will return a local file if it is less than a week old.
                    'any' will return the most recent file, if any exist.
    """
    abs_path = os.path.abspath(dir)

    if os.path.exists(abs_path) == True:
        print ("directory exists")
        print (abs_path)
    
    elif os.path.exists(abs_path) == False:
        print (f"No directory exists called: '{abs_path}'")
        while True:
            try:
                mk_new_dir = input ("Would you like to create one? ").strip().strip('"')
                if mk_new_dir.lower().startswith('y'):
                    os.makedirs(abs_path)
                    print (f"Created empty folder '{dir}'")
                    break;
                elif mk_new_dir.lower().startswith('n'):
                    print ("No further action.")
                    return;

            except Exception as error:
                print('Invalid Input. Please enter "Y" or "N" or "yes" or "no"')
                print (error)
                print ("")
                continue
    while True:
            try:
                f_type = f'*{file_type}'
                files = glob.glob(f"{abs_path}/{f_type}")

                oldest_file = min(files, key=os.path.getctime)
                latest_file = max(files, key=os.path.getctime)

                print (abs_path)
                print ("Oldest file:",oldest_file)
                print ("Latest file:",latest_file)

                if horizon=='any':
                    return latest_file;
                elif horizon!='any':
                    break;

            except ValueError as error:
                if str(error) == "min() arg is an empty sequence":
                    return;
                else:
                    raise error
    
    utc_now = datetime.utcnow()
    utc_today = utc_now.date()
    utc_now_str = utc_now.strftime('%Y-%m-%d,%M,%H,%S,%Z')
    utc_today_str = today.strftime('%Y-%m-%d')

    if horizon=='today':
        valid_date = re.compile(f'_{utc_today_str}..............{file_type}$')
        if (latest_file.endswith(f"{utc_today_str}.{file_type}")) or (valid_date.findall(latest_file)):
            print ("A file from today UTC exists.")

        elif not (latest_file.endswith(f"{utc_today_str}.{file_type}")) or not (valid_date.findall(latest_file)):
            print ("No existing file from today UTC.")
            latest_file = 'NA'

    elif horizon=='now':
        if utc_now_str in latest_file:
            print ("A file from current datetime UTC exists.")
        elif utc_now_str not in latest_file:
            print ("No existing file from right now UTC.")
            latest_file = 'NA'

    elif horizon=='yesterday':
        utc_yest = utc_today - timedelta(days=1)
        utc_yest_str = utc_yest.strftime('%Y-%m-%d')
        valid_date = re.compile(f'{utc_yest_str}..............{file_type}$')
        
        if (latest_file.endswith(f"{utc_yest_str}.{file_type}")) or (valid_date.findall(latest_file)):
            print ("A file from yesterday UTC exists.")
        elif not (latest_file.endswith(f"{utc_yest_str}.{file_type}")) or not (valid_date.findall(latest_file)):
            print ("No existing file from yesterday UTC.")
            latest_file = 'NA'

    elif horizon=='week':
        t_minus_7d = utc_now - timedelta(days=7)
        last_7_days = daterange_str(t_minus_7d, utc_now)

        valid_dates = []
        for day in last_7_days:
            valid_dates.append(re.compile(f'{day}..............{file_type}$'))

        if any (latest_file.endswith(f"{day}.{file_type}") for day in last_7_days) or (any (valid_date.findall(latest_file) for valid_date in valid_dates)):
            print (f"A file from the past 7 days UTC exists.")

        elif not any (latest_file.endswith(f"{day}.{file_type}") for day in last_7_days) or not (any (valid_date.findall(latest_file) for valid_date in valid_dates)):
            print ("No existing file from the past 7 days UTC.")
            latest_file = 'NA'

    return latest_file;

def get_recent(dir='csv_files',file_type='csv', horizon='today'):
    """
    Get the most recent file from a directory, up to an acceptable threshold.

    Arguements:
    dir         :   The local directory to check. Default is csv_files.
    file_type   :   The file extension. Default is csv.
    horizon     :   What is to be accepted as a recent file. 
                    Default='today' returns a local file if it matches today's date.
                    'now' will reject a local file if does not match the current datetime.
                    'yesterday' will accept a file from yesterday.
                    'week' will return a local file if it is less than a week old.
                    'any' will return the most recent file, if any exist.
    """
    if horizon=='now':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='today')

    elif horizon=='today':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='today')

    elif horizon=='yesterday':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='today')
        if latest_file=='NA':
            latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='yesterday')

    elif horizon=='week':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='today')
        if latest_file=='NA':
            latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='yesterday')
            if latest_file=='NA':
                latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='week')

    elif horizon=='any':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='any')

    return latest_file;


def last_col_first(df):
    """
    Reorders the columns of a pandas DataFrame.
    Brings the last column to the start (left) of the table.
    Leaves the other columns in their original order.
    df  :   a padas DataFrame.
    """
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    # df = df[cols]
    df = df.loc[:, cols]
    return df;

def change_tz_now(from_tz, to_tz):
    """
    Change the tz of the current datetime now with a tzinfo attribute.
    Display the current time in two timezones.

    dates   :   list of dates.
    from_tz :   timezone to change.
    to_tz   :   desired timezone.

    e.g.    from_tz = 'US/Pacific'
            to_tz = 'US/Eastern'
    To see all, enter: pytz.all_timezones
                   or: pytz.common_timezones
    """
    tz1 = pytz.timezone(from_tz)
    tz1_now = datetime.now(tz1)
    print (tz1_now)

    tz2 = pytz.timezone(to_tz)
    tz2_now = tz1_now.astimezone(tz2)
    print (tz2_now)
    return tz2_now

def utc_tz(date):
    utc_tz = pytz.timezone("UTC")

    if type(date) is str:
        date = datetime.strptime(date,'%Y-%m-%d')
        utc_date = date.astimezone(utc_tz)

    elif type(date) is datetime:
        date = date
        utc_date = date.astimezone(utc_tz)

    elif type(date) is pd.Timestamp:
        date = pd.to_datetime(date)
        utc_date = date.tz_convert(utc_tz)
        
    return utc_date;



def change_tz(arg,from_tz, to_tz):
    """
    Change the tz of a date or an array of dates the index of pandas DataFrame.
    Retrun a new Pandas DateTime index and either return the old DateTime index as a series or drop it.

    arg   :   list of dates or pandas datetime index or pandas series.
    from_tz :   timezone to change.
    to_tz   :   desired timezone.

    e.g.    from_tz = 'US/Pacific'
            to_tz = 'US/Eastern'

    To see all, enter: pytz.all_timezones
                   or: pytz.common_timezones
    """
    errmsgs = {}
    # pytz.utc
    while True:
        try:
            tz1 = pytz.timezone(from_tz)
            tz2 = pytz.timezone(to_tz)

        except pytz.UnknownTimeZoneError:
            print("Searching for TZ...")
            zones = pytz.common_timezones
            for z in list(zones):
                if (from_tz in z) and (from_tz not in list(zones)):
                    from_tz = z
                    print (f"Timezone: {z}")
                elif (to_tz in z) and (to_tz not in list(zones)):
                    to_tz = z
                    print (f"Timezone: {z}")
            tz1 = pytz.timezone(from_tz)
            tz2 = pytz.timezone(to_tz)

        if type(arg) is pd.DatetimeIndex:
            idx = arg
            try:
                tz1_idx = idx.tz_localize(tz1)
            except TypeError as error:
                already_tz = "Already tz-aware, use tz_convert to convert."
                if already_tz in error.args[0]:
                    print ("Existing datetimes already localized... Proceeding to change TZ.")

                    tz1_idx = idx
        
            df = pd.DataFrame(index=tz1_idx)

        elif type(arg) is pd.DataFrame:
            df = arg
            try:
                tz1_idx = df.index.tz_localize(tz1)
            except TypeError as error:
                already_tz = "Already tz-aware, use tz_convert to convert."
                if already_tz in error.args[0]:
                    print ("Existing datetimes already localized... Proceeding to change TZ.")

                    tz1_idx = df.index
                    df.index=pd.DatetimeIndex(tz1_idx)

        elif type(arg[1]) is datetime:
            date_lst = list(arg)
            df = pd.DataFrame(index=date_lst)

        elif type(arg[0]) is str:
            try:
                for d in arg:
                    date_lst = datetime.strptime(d,'%Y-%m-%d')
                    df = pd.DataFrame(index=date_lst)

            except ValueError as error:
                errmsgs = ("please use the date format '%Y-%m-%d' to avoid ambiguity")
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)
                # print ("Exception object:", exception_object)
                print (error)
                print (errmsgs)

        df.sort_index(ascending=True, inplace=True)

        try:    
            tz1_idx = df.index.tz_localize(tz1)
        except TypeError as error:
            already_tz = "Already tz-aware, use tz_convert to convert."
            if already_tz in error.args[0]:
                print ("Existing datetimes already localized... Proceeding to change TZ.")
                tz1_idx = df.index

        tz1_ame = from_tz.replace('/', '_')
        df[f"Dt_{tz1_ame}"] = tz1_idx

        tz2_idx =  tz1_idx.tz_convert(tz2)
        df.index = tz2_idx
        df.index.names = ['DateTime']
        if df.columns[0] != f"Dt_{tz1_ame}":
            df = last_col_first(df)

        return df;

def get_str_dates(start_date=None,end_date=None,utc=False):
    # utc_now = datetime.utcnow()
    today = date.today()
    td = today.strftime("%d-%m-%Y")
    today_dmy = str(td)
    if end_date==None:
        end_date = today_dmy

    elif type(end_date) is not str:
        end_date = end_date.strftime("%d-%m-%Y")

    if start_date==None:
        start_date = today - timedelta(days=365)
        start_date = start_date.strftime("%d-%m-%Y")
        start_date = str(start_date)

    elif type(start_date) is not str:
        start_date = start_date.strftime("%d-%m-%Y")

    if utc:
        start_date = to_utc(start_date)
        end_date = to_utc(end_date)
    
    print("Today's local TZ date:", today_dmy)
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
    pd.to_datetime(df.index)
    
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
    """
    Convert a date or datetime object to UTC datetime.
    """
    date = pd.to_datetime(date,utc=True)
    return date;

def first_day_of_current_year(time=False, utc=False):
    """
    Calculate the first date or datetime of the current year.
    If time=True, it will return the first microsecond of the current year.
    """
    if time:
        fdocy = datetime.now().replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
    else:
        fdocy = datetime.now().date().replace(month=1, day=1)
    if utc:
        fdocy = to_utc(fdocy)
    return fdocy;

def last_day_of_current_year(time=False,utc=False):
    """
    Calculate the first date or datetime of the current year.
    If time=True, it will return the last microsecond of the current year.
    """
    if time:
        ldocy = datetime.now().replace(month=12, day=31,hour=23,minute=59,second=59,microsecond=999999)
    else:
        ldocy = datetime.now().date().replace(month=12, day=31)
    if utc:
        ldocy = to_utc(ldocy)
    return ldocy;

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

def get_settle_dates(df=None, start_date=None, end_date=None, time=None, settles='last_fri',utc=False):
    """
    Add a Series of futures settlement dates for the DataFrame of a given security.

    If a DataFrame is passed and no start_date and end_date passed, the settle dates for the entire series is returned.

    If utc=True, the datetimestamp of settlement will be in UTC timezone format.
    """
    errors = {}

    if settles=='last_fri':
        
        sd, ed = get_str_dates(start_date=start_date,end_date=end_date, utc=utc)

        if (start_date==None) and (df!=None):
            start_date = df.index.min()
        else:
            start_date = sd

        if (end_date==None) and (df!=None):
            end_date = df.index.max()
        else:
            end_date = ed

        if utc==True:
            tz= 'UTC'
        else:
            tz= None

        date_range_df = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq='D',tz=tz))
        # date_range['Date'] = date_range.index.to_series()
        # date_range_df['DateTime'] = date_range_df.index.to_series()
        date_range_df['Date'] = date_range_df.index.date
        date_range_df

    while True:
        try:
            if settles=='last_fri':

                last_fris = last_fridays(date_range_df)
                last_fris = last_fris.drop_duplicates(ignore_index=False)
                last_fris_date = last_fris.set_index('Date', drop=False, inplace=False)
                last_fris_date.index = last_fris_date.index.strftime('%Y-%m-%d')
                last_fris_date['Date'] = last_fris_date.index.to_series()

                # settle_dt_lst = last_fris_date['Date'].unique().tolist()
                # settlements = pd.Series(last_fris_date['Date'].values,index=last_fris_date.Date).to_dict()
                settlements = pd.Series(last_fris_date['Date'].values,index=last_fris_date['Date']).to_dict()
                for key in list(settlements.keys()):
                    settlements[key] = 'CME Exp.'
                print("First settle date:",next(iter(settlements.items())))

                dates_to_remove = last_fris_date.loc[(~last_fris_date['Date'].astype(str).isin(date_range_df['Date'].astype(str)))]
                dates_to_remove = dates_to_remove['Date'].unique().tolist()
                for nul_date in dates_to_remove:
                    settlements.pop(nul_date, None)
                print ("Last settle date:",next(reversed(settlements.items())))

                last_fris['DateTime'] = last_fris.index.to_series()

            elif settles!='last_fri':
                errors[0] = ("\nInvalid settlement date type.")
                errors[1] = ("\nPlease input paramater: settles='last_fri or ask Saran to edit the source code to add more dates.'\n")
                raise NotImplementedError

        except Exception as error:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            # print ("Exception object:", exception_object)
            print (error)
            for e in errors.values():
                if e is not None:
                    print (e)
            break
        return
