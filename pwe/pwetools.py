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
from datetime import datetime,date,timedelta
import re
import glob
from tqdm import tqdm
from collections import ChainMap, OrderedDict

def read_pd_csv(f_path,low_memory=False, index_col=['DateTime'], parse_dates=['DateTime'],infer_datetime_format=True):
    df= pd.read_csv(f_path,low_memory=low_memory, index_col=index_col, parse_dates=parse_dates,infer_datetime_format=infer_datetime_format)
    tqdm.pandas(desc="Applying Transformation")
    df.progress_apply(lambda x: x)
    return df;

def pd_to_csv(df, f_name, folder='csv_files'):

    check_folder(folder)
    df.to_csv(f_name)
    tqdm.pandas(desc="Applying Transformation")
    df.progress_apply(lambda x: x)

    f_path = os.path.abspath(f_name)
    
    print (f"\nSaved csv to: \n{f_path}")
    return f_path;

def idx_to_dt(df):
    df.index=pd.DatetimeIndex(df.index)
    df.sort_index(ascending=True, inplace=True)
    df.index.names = ['DateTime']
    return df

def daterange(start_dt, end_dt):
    dates = []
    for d in range(int ((end_dt - start_dt).days)+1):
        dates.append(start_dt + timedelta(d))
    return dates;

def daterange_str_ymd(start_dt, end_dt):
    dates = []
    for d in range(int ((end_dt - start_dt).days)+1):
        dates.append((start_dt + timedelta(d)).strftime("%Y-%m-%d"))
    return dates;

def daterange_str_dmy(start_dt, end_dt):
    dates = []
    for d in range(int ((end_dt - start_dt).days)+1):
        dates.append((start_dt + timedelta(d)).strftime("%d-%m-%Y"))
    return dates;

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
    
    utc_now = pytz.utc.localize(datetime.utcnow())
    utc_today = utc_now.date()
    utc_now_str = utc_now.strftime('%Y-%m-%d,%M,%H,%S,%Z')
    utc_today_str = utc_today.strftime('%Y-%m-%d')

    if horizon=='today':
        valid_date = re.compile(f'{utc_today_str}..............{file_type}$')
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
        last_7_days_ymd = daterange_str_ymd(t_minus_7d, utc_now)
        last_7_days_dmy = daterange_str_dmy(t_minus_7d, utc_now)
        last_7_days = last_7_days_ymd + last_7_days_dmy

        valid_dates = []
        for day in last_7_days:
            valid_dates.append(re.compile(f'{day}..............{file_type}$'))

        if any (latest_file.endswith(f"{day}.{file_type}") for day in last_7_days) or (any (valid_date.findall(latest_file) for valid_date in valid_dates)):
            print (f"A file from the past 7 days UTC exists.")

        elif not any (latest_file.endswith(f"{day}.{file_type}") for day in last_7_days) or not (any (valid_date.findall(latest_file) for valid_date in valid_dates)):
            print ("No existing file from the past 7 days UTC.")
            latest_file = 'NA'

    return latest_file;

def find_recent(dir='csv_files',file_type='csv', horizon='today'):
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
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='now')

    elif horizon=='today':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='today')

    elif horizon=='yesterday':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='yesterday')

    elif horizon=='week':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='week')

    elif horizon=='any':
        latest_file = check_for_recent(dir=dir,file_type=file_type, horizon='any')

    print ("find_recent:", latest_file)
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
    latest_file = find_recent(dir=dir,file_type=file_type, horizon=horizon)

    if latest_file=='NA':
        print (f"No local file exists for the horizon: '{horizon}'")
        while True:
            try:
                if latest_file=='NA':
                    get_older = input ("Would you like to try for an older file? Y/N? ").strip().strip('"')

                    if get_older.lower().startswith('y'):
                        print ("What horizon would you like to try for?")
                        wht_hzn = input ("today, yesterday, week or any? Or Q to quit.  ").strip().strip('"')
                        
                        if wht_hzn.lower().startswith('t'):
                            hrzn = 'today'
                            latest_file = find_recent(dir=dir,file_type=file_type, horizon=hrzn)
                            if latest_file =='NA':
                                print (f"No local file exists for the horizon: '{hrzn}'")
                                continue
                            elif latest_file !='NA':
                                return latest_file;

                        elif wht_hzn.lower().startswith('y'):
                            hrzn = 'yesterday'
                            latest_file = find_recent(dir=dir,file_type=file_type, horizon=hrzn)
                            if latest_file =='NA':
                                print (f"No local file exists for the horizon: '{hrzn}'")
                                continue
                            elif latest_file !='NA':
                                return latest_file;

                        elif wht_hzn.lower().startswith('w'):
                            hrzn = 'week'
                            latest_file = find_recent(dir=dir,file_type=file_type, horizon=hrzn)
                            if latest_file =='NA':
                                print (f"No local file exists for the horizon: '{hrzn}'")
                                continue
                            elif latest_file !='NA':
                                return latest_file;

                        elif wht_hzn.lower().startswith('a'):
                            hrzn = 'any'
                            latest_file = find_recent(dir=dir,file_type=file_type, horizon=hrzn)
                            if latest_file =='NA':
                                print (f"No local file exists for the horizon: '{hrzn}'")
                                continue
                            elif latest_file !='NA':
                                return latest_file;

                        elif wht_hzn.lower().startswith('q'):
                            return latest_file =='NA';
                        else:
                            raise NotImplementedError("Invalid Input")
                        
                    elif get_older.lower().startswith('n'):
                        print ("No further action.")
                        return;
                    else:
                        raise NotImplementedError("Invalid Input")

                elif latest_file=='NA':
                    return latest_file;

            except NotImplementedError as error:
                print (error)
                print('Please enter "today,"(t) "yesterday,"(y) "week"(w) or "any"(a). Or "Q" to quit.')
                print ("")
                continue
    
    elif latest_file!='NA':
        print ("get_recent:", latest_file)
        return str(latest_file);

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

def get_tz(tz):
    """
    Pass a string and return  a pytz timezone object.
    This function can also infer the timezone from the city, if it is a substring of the timezone. e.g. 'Dubai' will return 'Asia/Dubai.'
    """
    try:
        t_z = pytz.timezone(tz)

    except pytz.UnknownTimeZoneError:
        print("Searching for TZ...")
        zones = pytz.common_timezones
        for z in list(zones):
            if (tz in z) and (tz not in list(zones)):
                tz = z
                print (f"Timezone: {z}")
        t_z = pytz.timezone(tz)

    return t_z;

def assign_tz(arg, tz, yearfirst=True, dayfirst=True):
    """
    Add a tz attribute to a tz naive date.
    tz  : a string name of the pytz timezone. e.g. 'UTC', or 'Asia/Dubai'.
        This function can also infer the timezone from the city, if it is a substring of the timezone. e.g. 'Dubai' will match 'Asia/Dubai.'
    yearfirst /dayfirst  : see: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    """
    while True:
        t_z = get_tz(tz)

        if type(arg) is str:
            arg = pd.to_datetime(arg, yearfirst=yearfirst, dayfirst=dayfirst)
            arg = arg.tz_localize(t_z)
            break

        elif (type(arg) is pd.Timestamp or isinstance(arg, pd._libs.tslibs.timestamps.Timestamp)) and arg.tzinfo == None:
            arg= arg.tz_localize(t_z)
            break

        elif type(arg) is datetime and arg.tzinfo == None:
            arg = t_z.localize(arg)
            break

        elif type(arg) is pd.DatetimeIndex:
            if arg.tzinfo == None:
                arg = arg.tz_localize(t_z)
            elif arg.tzinfo != None:
                print ("Index is already assigned to the timezone:",str(arg.tzinfo))
                print ("To convert it to a different timezone, use: change_tz")
                break

        elif type(arg) is pd.DataFrame:
            if arg.index.tzinfo == None:
                arg.index = arg.index.tz_localize(t_z)
            elif arg.index.tzinfo != None:
                print ("Index is already assigned to the timezone:",str(arg.index.tzinfo))
                print ("To convert it to a different timezone, use: change_tz")
                break
        
        elif arg.tzinfo != None:
            print ("Date is already assigned to the timezone:",str(arg.tzinfo))
            print ("To convert it to a different timezone, use: change_tz")
            break

        return arg;

def str_to_dt(arg, yearfirst=True, dayfirst=True):
    """
    Convert a string representation of a either a date, datetime object to a string.
    As a last resort, convert to a pandas datetime using dateutil parser.
    """
    if type(arg) is str:
        try:
            arg = datetime.strptime(arg,'%Y-%m-%d')
        except ValueError:
            try:
                arg = datetime.strptime(arg,'%d-%m-%Y')
                print (f"Assuming {arg} is D/M/Y format. Ensure this is correct. Recommend Y/M/D to avoid ambiguity.")
            except ValueError:
                try:
                    arg = datetime.strptime(arg, "%Y-%m-%d %H:%M:%S%z")
                except ValueError:
                    try:
                        arg = datetime.strptime(arg, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            arg = datetime.strptime(arg, "%Y-%m-%d %H:%M:%S.%f%z")
                        except ValueError:
                            try:
                                arg = datetime.strptime(arg, "%Y-%m-%d %H:%M:%S.%f")
                            except ValueError:
                                print (f"Assuming {arg} is D/M/Y format. Ensure this is correct. Recommend Y/M/D to avoid ambiguity.")
                                arg = pd.to_datetime(arg, yearfirst=yearfirst, dayfirst=dayfirst)
    return arg;

def dt_to_str(arg):
    """
    Convert a date, datetime to a string. Use isoformat as a last resort.
    """
    if type(arg) is datetime:
        try:
            arg = datetime.strftime(arg,'%Y-%m-%d')
        except ValueError:
            try:
                arg = datetime.strftime(arg,'%d-%m-%Y')
                print (f"Assuming {arg} is D/M/Y format. Ensure this is correct. Recommend Y/M/D to avoid ambiguity.")
            except ValueError:
                try:
                    arg = datetime.strftime(arg, "%Y-%m-%d %H:%M:%S%z")
                except ValueError:
                    try:
                        arg = datetime.strftime(arg, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            arg = datetime.strftime(arg, "%Y-%m-%d %H:%M:%S.%f%z")
                        except ValueError:
                            try:
                                arg = datetime.strftime(arg, "%Y-%m-%d %H:%M:%S.%f")
                            except ValueError:
                                print (f"Converting {arg} to isoformat.")
                                arg = arg.isoformat()
    return arg;

def is_utc(date, yearfirst=True, dayfirst=True):
    """
    Assert that datetime object is UTC and format it as a pandas datetime Timestamp.
    If it is not already tz aware, make it timezone aware by assigning it UTC a timezone attribute.
    """
    date = pd.to_datetime(date,utc=True, yearfirst=yearfirst, dayfirst=dayfirst)
    return date;

def to_utc(arg, yearfirst=True, dayfirst=True):
    """
    Convert a datetime object, a Timestamp, a pandas DateTimeIndex to UTC.
    Pass a dataframe as an arguement and it will convert the DateTimeIndex.

    Check if either a string, datetime or timestamp is TZ aware or TZ naive.
    Convert to UTC or else assign it to UTC if it is TZ naive.
    Caution: assumes any naive datetime object is already in UTC.
    If the time is not already in UTC and doesn't have any tz metadate, first, assign it a timezone attribute with tz_localize
    yearfirst /dayfirst  : see: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    """
    utc_tz = pytz.timezone("UTC")

    if type(arg) is str:
        arg = str_to_dt(arg, yearfirst=True, dayfirst=True)

        if str(arg.tzinfo) == 'UTC':
            print (f"{arg} is already in UTC.")
            return arg;
        elif arg.tzinfo == None:
            print (f"Assuming naive datetime: {arg} is already in UTC and labelling it as such. Ensure this is correct.")
            arg = utc_tz.localize(arg)
        elif arg.tzinfo!=None:
            print (f"Converting {arg.tzinfo} to UTC")
            arg = arg.astimezone(utc_tz)

    elif type(arg) is datetime:
        if str(arg.tzinfo) == 'UTC':
            print (f"{arg} already in UTC.")
            return arg;
        elif arg.tzinfo == None:
            print (f"Assuming naive datetime: {arg} is already in UTC and labelling it as such. Ensure this is correct.")
            arg = utc_tz.localize(arg)
        elif arg.tzinfo!=None:
            print (f"Converting {arg.tzinfo} to UTC")
            arg = arg.astimezone(utc_tz)

    elif type(arg) is pd.Timestamp:
        if str(arg.tzinfo) == 'UTC' or str(arg.tzinfo) == 'tzutc()':
            print (f"{arg} already in UTC.")
            return arg;
        elif arg.tzinfo == None:
            print (f"Assuming naive datetime: {arg} is already in UTC and labelling it as such. Ensure this is correct.")
            arg = pd.to_datetime(arg, utc=True, yearfirst=yearfirst, dayfirst=dayfirst)
        elif arg.tzinfo!=None:
            print (f"Converting {arg.tzinfo} to UTC")
            arg = arg.tz_convert(utc_tz)

    elif type(arg) is pd.DatetimeIndex:
        if str(arg.tzinfo) == 'UTC':
            print ("Index already in UTC.")
            return arg;
        elif arg.tzinfo == None:
            print (f"Assuming naive DateTime Index is already in UTC and labelling it as such. Ensure this is correct.")
            arg = arg.tz_localize(utc_tz)
        elif arg.tzinfo != None:
            print (f"Converting {arg.tzinfo} to UTC")
            arg = arg.tz_convert(utc_tz)

    elif type(arg) is pd.DataFrame:
        if str(arg.index.tzinfo) == 'UTC':
            print ("Index already in UTC.")
            return arg;
        if arg.index.tzinfo == None:
            print (f"Assuming naive DateTime Index is already in UTC and labelling it as such. Ensure this is correct.")
            arg.index = arg.index.tz_localize(utc_tz)
        elif arg.index.tzinfo != None:
            print (f"Converting {str(arg.index.tzinfo)} to UTC")
            arg.index = arg.index.tz_convert(utc_tz)

    return arg;

def change_tz(arg,from_tz, to_tz):
    """
    Change the tz of a date or an array of dates the index of pandas DataFrame.
    Retrun a new Pandas DateTime index and either return the old DateTime index as a series or drop it.
    If a single datetime or timestamp is passed, it will return a datetime or timestamp.
    This function can also infer the timezone from the city, if it is a substring of the timezone. e.g. 'Dubai' will match 'Asia/Dubai.'

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
        if issubclass(type(from_tz), pytz.BaseTzInfo):
            tz1 = from_tz
        else:
            try:
                tz1 = pytz.timezone(from_tz)

            except pytz.UnknownTimeZoneError:
                print("Searching for TZ...")
                zones = pytz.common_timezones
                for z in list(zones):
                    if (from_tz in z) and (from_tz not in list(zones)):
                        from_tz = z
                        print (f"Timezone: {z}")
                tz1 = pytz.timezone(from_tz)

        if issubclass(type(to_tz), pytz.BaseTzInfo):
            tz2 = to_tz
        else:
            try:
                tz2 = pytz.timezone(to_tz)

            except pytz.UnknownTimeZoneError:
                print("Searching for TZ...")
                zones = pytz.common_timezones
                for z in list(zones):
                    if (to_tz in z) and (to_tz not in list(zones)):
                        to_tz = z
                        print (f"Timezone: {z}")
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

        elif (type(arg) is pd.Timestamp or isinstance(arg, pd._libs.tslibs.timestamps.Timestamp)):
            try:
                arg = arg.tz_localize(tz1)
            except TypeError as error:
                already_tz = "Cannot localize tz-aware Timestamp, use tz_convert for conversions"
                if already_tz in error.args[0]:
                    print ("Timestamp already localized... Proceeding to change TZ.")
                    arg.tz_convert(tz2)
            return arg;

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

        tz1_name = from_tz.replace('/', '_')
        df[f"Dt_{tz1_name}"] = tz1_idx

        tz2_idx =  tz1_idx.tz_convert(tz2)
        df.index = tz2_idx
        df.index.names = ['DateTime']
        if df.columns[0] != f"Dt_{tz1_name}":
            df = last_col_first(df)

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

def get_str_dates(start_date=None,end_date=None, tz=None):
    if tz==None:
        today = datetime.now().astimezone()
    else:
        if issubclass(type(tz), pytz.BaseTzInfo):
            t_z = tz
        else:
            t_z = get_tz(tz)
        today = t_z.localize(datetime.utcnow())
    today_str = today.isoformat()

    if end_date==None:
        end_date = today_str

    elif type(end_date) is not str:
        end_date = dt_to_str(end_date)

    if start_date==None:
        start_date = today - timedelta(days=365)
        start_date = start_date.isoformat()

    elif type(start_date) is not str:
        start_date = dt_to_str(start_date)
    
    # print("Today's date:", today_str)
    # print(" ")
    # print("Start date:", start_date)
    # print("End date:", end_date)
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

def sort_index(df, utc=True, yearfirst=True, dayfirst=True):
    df.index=pd.DatetimeIndex(df.index)
    pd.to_datetime(df.index, yearfirst=yearfirst, dayfirst=dayfirst)
    
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
    tqdm.pandas(desc="Applying Transformation")
    df.progress_apply(lambda x: x)
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
        fdocy = is_utc(fdocy)
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
        ldocy = is_utc(ldocy)
    return ldocy;

def split_datetime(df, date=True,day=False,month=False,year=False,time=False):
    if date:
        df['Date'] = df.index.date
    if day:
        df['Day'] = df.index.day
    if month:
        df['Month'] = df.index.month
    if year:
        df['Year'] = df.index.year
    if time:
        df['Time'] = df.index.time
    return;

def diff_between_df(df1,df2):
    diff = pd.concat([df1,df2]).drop_duplicates(keep=False)
    return diff;

def missing_from_df(df1,df2):
    diff =  diff_between_df(df1,df2)

    df1_miss = df1.loc[(df1.index.isin(diff.index.astype(str)))]
    n_df1_miss = len(df1_miss.index)
    print ("Missing from df1:", n_df1_miss)

    df2_miss = df2.loc[(df2.index.isin(diff.index.astype(str)))]
    n_df2_miss = len(df2_miss.index)
    print ("Missing from df2:", n_df2_miss)

    return df1_miss, df2_miss;

def get_unique_dates(df, yearfirst=True, dayfirst=True):
    uniq = df.index.date
    uni = pd.DataFrame(uniq, index=uniq)
    unique = pd.DataFrame(uni.index.unique(), index=uni.index.unique(), columns=['Unique Date'])
    unique.index = pd.to_datetime(unique.index, yearfirst=yearfirst, dayfirst=dayfirst)
    unique.index.names = ['DateTime']
    print ("Unique dates:", len(unique.index))
    return unique;

def count_df_dupes_idx(df, keep='first'):
    dupes_bool = df.index.duplicated(keep=keep)
    dupes = np.sum(dupes_bool)

    if dupes > 0:
        bin_count = np.bincount(dupes_bool)
        dupes = bin_count[1]
        non_dupes = bin_count[0]
        dupe_perc = dupes / non_dupes

        df_dupes = df.loc[dupes_bool]
        dupe_start = df_dupes.index.date.min()
        dupe_end = df_dupes.index.date.max()

        print (f"Duplicate rows: {dupes}","({:.6%})".format(dupe_perc), f"between {dupe_start} and {dupe_end}")
    elif dupes == 0:
        print ("No duplicate rows.")
    return dupes;

def get_dupes_df(df):
    dupes_df = df.loc[df.duplicated()==True]
    return dupes_df;

def concat_non_dupe_idx(df1, df2):
    """
    Concatenate two dataframes.
    If any duplicated index rows exist, display the start and end (date) of the duplicated range, and display the % of duplicates.
    Remove the duplicates, if any exist.
    Useful for updating a dataset periodically without needing to know the last entry in the existing local dataset.
    """
    if ((df1 is not None and not isinstance(df1, pd.core.frame.DataFrame)) or (df2 is not None and not isinstance(df2, pd.core.frame.DataFrame))):
        raise ValueError('df1 and df2 must be of type pandas.core.frame.DataFrame.')

    if (df1 is None):
        df = df2
        return df;

    if (df2 is None):
        df = df1
        return df1;

    elif(df1 is not None) and (df2 is not None):
        df = pd.concat([df1, df2])

        dupes = count_df_dupes_idx(df, keep='first')

        if dupes > 0:
            print ("Removing duplicates...")    
            # new_idx = df.index.drop_duplicates(keep=False)
            # df = df[~dupes_bool]
            #df = df.drop_duplicates(keep='first')
            df_new = df[~df.index.duplicated(keep='first')]
            df.sort_index(ascending=True, inplace=True)
            print ("Removed duplicates.") 
            return df_new;

    
def get_missing_dates(df):
    if type(df.index) != 'DatetimeIndex':
        missing_dates = pd.date_range(start = df.index.min(), end = df.index.max() ).difference(df.index)
        missing_dates = pd.DataFrame(missing_dates, columns=['Missing DateTime'], index=pd.DatetimeIndex(missing_dates))
        n_miss = len(missing_dates.index)
        print ("Missing Datetimes:", n_miss)

        unique = get_unique_dates(missing_dates)
        unique = unique.rename(columns={'Unique Date': 'Missing Date'})
        return missing_dates, unique;
    else:
        print ("Index is not in Datetime format")

def common_missing_dates(df1,df2):
    if df1.equals(df2) == False:
        print ("Dataframes are not equal...")
    elif df1.equals(df2) == True:
        print ("Dataframes are equal...")
    df1_miss,df1_uni_miss = get_missing_dates(df1)
    df2_miss,df2_uni_miss = get_missing_dates(df2)

    common = df1_miss.loc[(df1_miss.index.astype(str).isin(df2_miss.index.astype(str)))]
    common = common.rename(columns={'Missing DateTime': 'Common Missing DateTime'})
    print ("Common missing Datetimes:", len(common.index))
    common_dates = get_unique_dates(common)
    print ("Common missing dates:", len(common_dates.index))
    common_dates = common_dates.rename(columns={'Unique Date': 'Common Missing Date'})
    return common, common_dates;

def go_to_date(df, date):
    """
    Returns a single row based on a provided index name (typically Date or Datetime)
    date    : (str) e.g. date="2021-02-01 00:00:00+00:00"
    """
    return df.loc[df.index.astype(str)==date]

def concat_summary(df_new, df_old):
    new_miss, new_miss_uni = get_missing_dates(df_new)
    common_miss, common_miss_dates = common_missing_dates(df_new, df_old)
    count_df_dupes_idx(df_new)
    return new_miss, new_miss_uni, common_miss, common_miss_dates

def last_fridays(df, time=False):
    # df['Day'] = df.index.day
    # df['Month'] = df.index.month
    # df['Year'] = df.index.year
    # #df['Time'] = df.index.time
    # df['Date'] = pd.to_datetime(df[['Year','Month','Day']])
    #df['DateTime'] = pd.to_datetime(df[['Year','Month','Day','Time']])
    if time==False:
        split_datetime(df, date=True,day=False,month=False,year=False,time=False)
        last_fris = pd.DataFrame(df.apply(lambda x: x['Date'] + pd.offsets.LastWeekOfMonth(n=1,weekday=4), axis=1), columns=['Date'])
    elif time:
        last_fris = pd.DataFrame(df.apply(lambda x: x['DateTime'] + pd.offsets.LastWeekOfMonth(n=1,weekday=4), axis=1), columns=['DateTime'])

    return last_fris;

def get_exp_dates(df=None, start=None, end=None, freq='h', time=None, exp_tz='UTC', expires='last_fri', name='CME Exp.'):
    """
    Add a Series of futures expiration dates for the DataFrame of a given security.

    If a DataFrame is passed and no start_date and end_date passed, the settle dates for the entire series is returned.

    If utc=True, the datetimestamp of expiration will be in UTC timezone format.

    start, end  : the start and end dates. If a string, the dates are assumed to be in UTC.

    expires :   A setting to specify the expiration date interval. Currently only supports 'last_fri' but can easily be expanded.

    time    :   The expiration time (either local or UTC. Does not need to match tz to tz of dataset)
                e.g. If the dataset is formatted in UTC and the contract expires at 4pm London time, you can input '16:00:00' and set the tz to 'London.'
                It will account for daylight saving and return Expiration_DateTimes in UTC.
                format: string - '%H:%M:%S'

    freq    :   the interval of the timeseries. Defaultis 'h' for hours. 'm' forminutes, 'd'for days. 'ms' for microseconds etc., as per pandas date_range function.

    exp_tz :   The timezone of the expiration time.

    name    :   The name of the expiration for chart anotation purposes.

    Returns:    a dict of settlemet dates to use as annotations on a chart.
                a pandas DataFrame of the settlemt dates as a series.
    """
    errors = {}

    if exp_tz == 'UTC':
        exp_tz= 'UTC'
    elif exp_tz != 'UTC' and exp_tz!=None:
        exp_tz = get_tz(exp_tz)
    elif exp_tz ==None:
        exp_tz= None

    if expires=='last_fri':
        
        if start!=None:
                sd = pd.to_datetime(start, utc=True)
                sd = sd.tz_convert(exp_tz)
        if end!=None:
            ed = pd.to_datetime(end, utc=True)
            ed = ed.tz_convert(exp_tz)

        if start==None and isinstance(df, pd.DataFrame):
            start_date = df.index.min()
            start_date = pd.to_datetime(start_date, utc=True)
            start_date = start_date.tz_convert(exp_tz)

        else:
            start_date = sd
            print("Start date:", start_date)

        if end==None and isinstance(df, pd.DataFrame):
            end_date = df.index.max()
            end_date = pd.to_datetime(end_date, utc=True)
            end_date = end_date.tz_convert(exp_tz)

        else:
            end_date = ed
            print("End date:", end_date)

        if (time==None) or (freq=='D'):
            date_range_df = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq='D',tz=exp_tz))
            date_range_df.index = pd.to_datetime(date_range_df.index, utc=True)
            # date_range['Date'] = date_range.index.to_series()
            # date_range_df['DateTime'] = date_range_df.index.to_series()
            date_range_df['Date'] = date_range_df.index.date
            date_range_df['DateTime'] = date_range_df.index
            range_df = date_range_df

        elif freq!='D' and time!=None:
            dt_range_df = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq=freq,tz=exp_tz))
            dt_range_df['Time'] = dt_range_df.index.time
            dt_range_df['Exp_DateTime'] = dt_range_df['Time'].astype(str) == time
            dt_range_df = dt_range_df.loc[dt_range_df['Exp_DateTime'] == True]
            dt_range_df.index = pd.to_datetime(dt_range_df.index, utc=True)
            dt_range_df['DateTime'] = dt_range_df.index
            dt_range_df = dt_range_df.drop(columns=['Time', 'Exp_DateTime'])
            range_df = dt_range_df

    while True:
        try:
            if expires=='last_fri':

                if (time==None) or (freq=='D'):
                    last_fris = last_fridays(range_df)
                    last_fris = last_fris.drop_duplicates(ignore_index=False)
                    last_fris_df = last_fris.set_index('Date', drop=False, inplace=False)
                    last_fris_df.index = last_fris_df.index.strftime('%Y-%m-%d')
                    last_fris_df['Date'] = last_fris_df.index.to_series()

                    expirations = pd.Series(last_fris_df['Date'].values,index=last_fris_df['Date']).to_dict()
                    for key in list(expirations.keys()):
                        expirations[key] = name

                    dates_to_remove = last_fris_df.loc[(~last_fris_df['Date'].astype(str).isin(range_df['Date'].astype(str)))]
                    hist_exp_df = last_fris_df.loc[(~last_fris_df['Date'].astype(str).isin(dates_to_remove['Date'].astype(str)))]
                    removal_lst = dates_to_remove['Date'].unique().tolist()
                    for nul_date in removal_lst:
                        expirations.pop(nul_date, None)
                    print("")
                    print("First expiration date:",next(iter(expirations.items())))
                    print ("Last expiration date:",next(reversed(expirations.items())))

                    hist_exp_df['Date'] = hist_exp_df.index.to_series()
                    break

                elif (time!=None):
                    last_fris = last_fridays(range_df, time=True)
                    last_fris = last_fris.drop_duplicates(ignore_index=False)
                    last_fris_df = last_fris.set_index('DateTime', drop=False, inplace=False)
                    last_fris_df['DateTime'] = last_fris_df.index.to_series()

                    str_exp_df = pd.DataFrame(last_fris_df.index.strftime('%Y-%m-%d %H:%M:%S'), index= last_fris_df.index.strftime('%Y-%m-%d %H:%M:%S'), columns=['DateTime'])

                    expirations = pd.Series(str_exp_df['DateTime'].values,index=str_exp_df['DateTime']).to_dict()
                    for key in list(expirations.keys()):
                        expirations[key] = name
                    print("")
                    print("First Expiration_DateTime:",next(iter(expirations.items())))

                    dates_to_remove = last_fris_df.loc[(~last_fris_df['DateTime'].astype(str).isin(range_df['DateTime'].astype(str)))]
                    hist_exp_df = last_fris_df.loc[(~last_fris_df['DateTime'].astype(str).isin(dates_to_remove['DateTime'].astype(str)))]

                    dates_to_remove['DateTime'] = dates_to_remove['DateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    removal_lst = dates_to_remove['DateTime'].unique().tolist()
                    for nul_date in removal_lst:
                        expirations.pop(nul_date, None)
                    print ("Last expiration date:",next(reversed(expirations.items())))

                    hist_exp_df['DateTime'] = hist_exp_df.index.to_series()
                    break

                elif expires!='last_fri':
                    errors[0] = ("\nInvalid expiration date type.")
                    errors[1] = ("\nPlease input paramater: expires='last_fri or ask Saran to edit the source code to add more dates.'\n")
                    raise NotImplementedError

            elif expires!='last_fri':
                errors[0] = ("\nInvalid expiration date type.")
                errors[1] = ("\nPlease input paramater: expires='last_fri or ask Saran to edit the source code to add more dates.'\n")
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

    if (time==None) or (freq=='D'):
        df = add_settle_dates(df, hist_exp_df)
    elif freq!='D' and time!=None:
        df = add_settle_dates(df, hist_exp_df, time=True)

    return expirations, last_fris_df, df;

def add_settle_dates(df, hist_exp_df, time=False):
    if time==False:
        if 'Date' not in df:
            df['Date'] = df.index.date
        df['Is_Exp_Date'] = df['Date'].astype(str).isin(hist_exp_df['Date'])
        df.tail()
        df['Is_Exp_Date'].value_counts()
        print ("Expiration dates in range:", hist_exp_df['Date'].count())

        df['Exp_Date'] = df[df['Is_Exp_Date']==True]['Date']
        found_set_dates = pd.DataFrame(df['Exp_Date'], columns=['Exp_Date']).drop_duplicates()
        print ("Found expiration dates:", found_set_dates['Exp_Date'].count())

        missing_set_date = hist_exp_df.loc[(~hist_exp_df['Date'].isin(found_set_dates['Exp_Date'].astype(str)))]
        print ("Missing expiration dates:", len(missing_set_date))

    elif time:
        if 'DateTime' not in df:
            df['DateTime'] = df.index
        df['Is_Exp_DateTime'] = df['DateTime'].astype(str).isin(hist_exp_df['DateTime'].astype(str))
        df.tail()
        df['Is_Exp_DateTime'].value_counts()

        valid_exp_dates = pd.DataFrame(hist_exp_df.index.date, columns=['Date'])
        valid_exp_dates = valid_exp_dates.drop_duplicates(ignore_index=False)

        print ("Expiration dates in range:", (valid_exp_dates['Date'].count()))
        print ("Expiration day datetimes in range:", (hist_exp_df['DateTime'].count()))

        df['Exp_DateTime'] = df[df['Is_Exp_DateTime']==True]['DateTime']
        print ("Found expiration day datetimes:", df['Exp_DateTime'].count())

        missing_set_date = hist_exp_df.loc[(~hist_exp_df['DateTime'].astype(str).isin(df['Exp_DateTime'].astype(str)))]
        print ("Missing expiration day datetimes:", len(missing_set_date))

    return df;

def get_t_delta(interval='h'):
    if interval=='h':
        t_delta = 'timedelta64[h]'
    elif interval=='d':
        t_delta = 'timedelta64[d]'
    elif interval=='m':
        t_delta = 'timedelta64[m]'
    elif interval=='ms':
        t_delta = 'timedelta64[ms]'
    elif interval=='ns':
        t_delta = 'timedelta64[ns]'
    return t_delta;

def t_to_exp(df, interval='h'):
    df['Next_Exp'] = df['Exp_DateTime'].bfill()
    t_delta = get_t_delta(interval=interval)
    df['t_to_Exp'] = (df['Next_Exp']-df['DateTime']).astype(t_delta)
    return df;

def t_since_exp(df, interval='h'):
    df['Last_Exp'] = df['Exp_DateTime'].ffill()
    t_delta = get_t_delta(interval=interval)
    df['t_since_Exp'] = (df['DateTime']-df['Last_Exp']).astype(t_delta)
    return df;

def expir_delta(df, interval='h'):
    """
    Add columns expressing the timedelta since expiration and until the next expiration.

    df          : a pandas DataFrame.
    interval    : the format to express the timedelta. Default is 'h' for hours.
                  d, h, m, ms, ns.
    """
    t_to_exp(df, interval=interval)
    t_since_exp(df, interval=interval)

def get_exp_range(df, t=48, t_til=None, t_since=None):
    """
    Return a subseries of datetime ranges, either a specified max timeframe before expiry or after expiry, for every contract period in the series.
    Alternatively, select slices of datetimes before and after expiry.
    t   :   int. e.g. Enter -20 to get the 20 periods before each expiry date. Or +20 to get the 20 periods after expiry, for every contract period in the series..
    
    Alternativly, enter both t_til and t_since values and ignore the t paramater.
            e.g t_til=20 and t_since=20 will return the 40 periods either side of the expiry date or datetime.
    """
    if t!=None and t_since==None and t_til==None:
        if t < 0:
            t_minus = t*-1
            df_t_exp = df.loc[df['t_to_Exp']<=t_minus]
        if t > 0:
            df_t_exp = df.loc[df['t_since_Exp']<=t]
        if t == 0:
            df_t_exp = df.loc[df['t_since_Exp']==0]

    elif t_since!=None and t_til!=None:
        df_t_exp = df.loc[(df['t_to_Exp']<=t_til) & (df['t_since_Exp']<=t_since)]

    else:
        raise NotImplementedError("Input either -t or +t, or else input both +t_til and +t_since.")

    return  df_t_exp;

def get_exp_t(df, t=0, t_til=None, t_since=None):
    """
    Return a subseries of single datetimes, at a specified timeframe before expiry or after expiry.
    Alternatively, select a subseries comprising a datetime before expiry and another one after expiry, for every contract period in the series.
    t   :   int. e.g. Enter -20 to get a set of the exact t-20 datetime before each expiry date. Or +20 to get a set of the exact t+20 datetimes after expiry.
    
    Alternativly, enter both t_til and t_since values and ignore the t paramater.
            e.g t_til=20 and t_since=20 will return both the exact t-20 datetimes before expiration and the exact t+20 datetimes after expiration.
    """
    if t!=None and t_since==None and t_til==None:
        if t < 0:
            t_minus = t*-1
            df_t_exp = df.loc[df['t_to_Exp']==t_minus]
        if t > 0:
            df_t_exp = df.loc[df['t_since_Exp']==t]
        if t == 0:
            df_t_exp = df.loc[df['t_since_Exp']==0]

    elif t_since!=None and t_til!=None:
        df_t_exp = df.loc[(df['t_to_Exp']==t_til) & (df['t_since_Exp']==t_since)]

    else:
        raise NotImplementedError("Input either -t or +t, or else input both +t_til and +t_since.")

    return  df_t_exp;

def get_exp_t_ordered(df, t=24):
  """
  Input a pandas DataFrame and specify a timedelta.
  Returns a ordered dict of DataFrames.
  Each DataFrame in the ordered dict is a subseries of single datetimes, at a specified timeframe before expiry or after expiry.
  Alternatively, select a subseries comprising a datetime before expiry and another one after expiry, for every contract period in the series.

  t   :   int. e.g. Enter -20 to get a set of the exact t-20 datetime before each expiry date. Or +20 to get a set of the exact t+20 datetimes after expiry.
          This function will itterativley create DataFrames for each t+- step from t to t=0. 
          i.e. if t=20, 20 DataFrames will be created.

    To unpack the dict, use: globals().update(dict_df_exps)
  """
  # dict_df_exps = {}
  dict_df_exps = OrderedDict()
  df_name = df.name.strip().replace('/', '_').replace(' ', '_').lower()
  if t>0:
    t= t+1
    for t in range(1, t):
      key = "{name}_t_plus_{t_}".format(name=df_name,t_=t)
      _df_t = get_exp_t(df, t=t, t_til=None, t_since=None)
      dict_df_exps[key] = _df_t

  elif t<0:
    for t in range(t, 1, 1):
      key = "{name}_t_min_{t_}".format(name=df_name, t_=abs(t))
      _df_t = get_exp_t(df, t=t, t_til=None, t_since=None)
      dict_df_exps[key] = _df_t

  elif t==0:
    print("t=0 is only one subseries. No dict needed. Use: get_exp_t(df, t=0)")
      
  print ([*dict_df_exps])
  return dict_df_exps;

def drop_rows(df, head=False, tail=True, n=1):
    """
    Drop either the first n rows or the last n rows (or both) of a pandas DataFrame.
    Default is set to drop the last row.
    """
    if head:
        df = df.drop(df.head(n).index,inplace=True)
    if tail:
        df= df.drop(df.tail(n).index,inplace=True)
    return df;