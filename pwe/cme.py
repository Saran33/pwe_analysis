#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 09:11:11 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import os
import time
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta, tzinfo
from pwe.pwetools import check_folder, pd_to_csv, get_recent, concat_non_dupe_idx, idx_to_dt, read_pd_csv

import datamine.io as dm
from pprint import pprint as pp


def download_cme(username, password, path='./data2/', folder='csv_files/CME/Crypto/full_datasets', limit=2, dataset='CRYPTOCURRENCY', processes=1):
    """
    Establish an object to interact with CME Datamine.
    Supply Credentials per Documentation: http://www.cmegroup.com/market-data/datamine-api.html
    Params:
    processes: The pulls are multithreaded to speed them up; you can adjust this by adjusting the processes in the MyDatamine object.
    folder:  The name of the local directory for saving CSV files. Ensure that it is reserved only for CME data. 
            Do not maually alter the csv file names. The file names are read to determine the most recent csv.
    """
    myDatamine = dm.DatamineCon(
        username=username, password=password, path=path)

    myDatamine.get_catalog(dataset=dataset, limit=limit)
    myDatamine.data_catalog.popitem()

    dataCatalogDF = pd.DataFrame.from_dict(myDatamine.data_catalog,).T
    dataCatalogDF.dataset.value_counts()
    dataCatalogDF

    myDatamine.processes = processes
    if dataset == 'CRYPTOCURRENCY':
        myDatamine.crypto_load(download=False)
        myDatamine.crypto_DF.index = pd.to_datetime(myDatamine.crypto_DF.index)
        myDatamine.crypto_DF.symbol.value_counts()
        myDatamine.crypto_DF.index = pd.to_datetime(myDatamine.crypto_DF.index)
        myDatamine.crypto_DF.symbol.value_counts()
        myDatamine.crypto_DF.head()
        cme_df = myDatamine.crypto_DF

        new_cme_f_name = new_cme_fpath(
            cme_df, dataset='CRYPTOCURRENCY', dir=folder)
        pd_to_csv(df=cme_df, folder=folder, f_name=new_cme_f_name)

        #cme_df.index = pd.to_datetime(cme_df.index)

    return cme_df


def new_cme_fpath(cme_df, dataset='CRYPTOCURRENCY', dir='csv_files/CME/Crypto'):
    """
    Check the dates and times of the CME dataframe and format the file name accordingly.
    """
    cme_start = cme_df.index.min()
    print(cme_start)
    cme_end = cme_df.index.max()
    print(cme_end)

    cme_fdate_start = cme_start.strftime('%Y-%m-%d')
    cme_fdate_end = cme_end.strftime('%Y-%m-%d')
    print(cme_fdate_start)
    print(cme_fdate_end)

    cme_f_date = None

    if (cme_fdate_start == cme_fdate_end) and (cme_end - cme_start) == timedelta(hours=23, minutes=59, seconds=59):

        cme_f_date = cme_fdate_end
        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_f_date}.csv'

    elif (cme_fdate_start == cme_fdate_end) and (cme_end - cme_start) == timedelta(hours=23, minutes=59, seconds=58):
        cme_f_date = cme_fdate_end
        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_f_date}.csv'

    elif (cme_fdate_start != cme_fdate_end) and ((str(cme_start.time()) == "00:00:00") and (str(cme_end.time()) == "23:59:59")):

        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_fdate_start}_{cme_fdate_end}.csv'

    elif (cme_fdate_start != cme_fdate_end) and ((str(cme_start.time()) != "00:00:00") or (str(cme_end.time()) != "23:59:59")):
        cme_fdt_start = cme_start.strftime('%Y-%m-%d,%M,%H,%S,%Z')
        cme_fdt_end = cme_end.strftime('%Y-%m-%d,%M,%H,%S,%Z')
        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_fdt_start}_{cme_fdt_end}.csv'
    else:
        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_fdate_start}_{cme_fdate_end}.csv'
        print("Date format issue. Double check the start and end dates suppplied by CME. Are they an uneven interval?")
        print("Saving anyway.")

    return new_cme_f_name


def extract_cme_df(cme_df, symbol, folder='csv_files/CME/Crypto'):
    """
    Extract the relevent security into dataframe.
    symbol  : (str) - the relevent ticker. e.g. "BRR" , "BRTI".
    """
    df = pd.DataFrame(cme_df.loc[cme_df['symbol'] == symbol, 'mdEntryPx'])

    df.rename(columns={'mdEntryPx': symbol}, inplace=True)
    df.columns = df.columns.str.strip().str.upper().str.replace(
        ' ', '_').str.replace('(', '').str.replace(')', '')

    df = idx_to_dt(df)

    check_folder(f'{folder}/temp')
    dir_rel = f'{folder}/temp'
    f_path = new_cme_fpath(df, dataset=symbol, dir=dir_rel)
    print(f"\nSaving new {symbol} data to:\n", f_path)
    pd_to_csv(df, f_path, folder=dir_rel)

    return df


def get_cme(username, password, dataset='CRYPTOCURRENCY', hzn='any', dir='csv_files/CME/Crypto', index_col='DateTime', limit=2,
            processes=1, resample=True, interval='1h', symbols=None):
    """
    Establish an object to interact with CME Datamine.
    Supply Credentials per Documentation: http://www.cmegroup.com/market-data/datamine-api.html
    Download CME Datamine data, import it into a project in a padas dataframe and save it to csv.
    If the data already exists locally, combine the new data with the most recent existing csv.
    If no new data exists, and a local file exists, import from local file.

    Arguements:
    dataset     :   The desired dataset, as per CME Datamine API name.
    limit       :   The number of most recent items to downnload. Default is 2 (metadata item and the most recet day of data.)
    path        :   The name of local directory for savig the unformatted JSON data.
    processes   :   The pulls are multithreaded to speed them up; you can adjust this by adjusting the processes in the MyDatamine object.

    dir         :   The local directory to check. Default is csv_files.
    file_type   :   The file extension. Default is csv.
    hzn         :   Horizon - The oldest datetime to be accepted as a "recent" file. 
                    Default='today' returns a local file if it matches today's date. If no local file exists from today, it will check for new data.
                    'now' will reject a local file if does not match the current datetime.
                    'yesterday' will accept a file from yesterday.
                    'week' will return a local file if it is less than a week old.
                    'any' will return the most recent local file, if any exist.
    resample    :   If True, any minute timeseries will be resampled to a 1h timeseries and both the 1m and 1h series will be saved to csvs. 
    interval    :   If '1h' is selected, and horizon='any', 1h data will be returned, and the comutationally expensive reading of 1m data wil be forgone.
                    If '1h' is selected, and horizon is not 'any', then the resample arguemet will =True.

    symbols     :   The tickers of interest. e.g. 'BRR' 'BRTI or ['BRR, 'BRTI']

    Returns     :   For cryptocurrency: it returns a dataframe for BRR and BRTI 1h. It also saves the entire crypto dataset, as well as BRR, BRTI 1m and BRTI 1h.
                                        Currrently, to access ETH, the dataset can be read from CSV manually.

    """

    if dataset == 'CRYPTOCURRENCY':

        brr_dir = f"{dir}/BRR"
        brti_1m_dir = f"{dir}/BRTI/1m"
        brti_1h_dir = f"{dir}/BRTI/1h"

        if (symbols == None) or ('BRR' in symbols):

            print("Searching:", brr_dir)
            try:
                brr_old_f = get_recent(
                    dir=brr_dir, file_type='csv', horizon=hzn)
            except ValueError as error:
                if str(error) == "Invalid file path or buffer object type: <class 'NoneType'>":
                    print("Download aborted.")
                    ans1 = [None, None]
                    return ans1
            print(brr_old_f)
            try:
                brr_old = pd.read_csv(brr_old_f, low_memory=False, index_col=[
                                      index_col], parse_dates=[index_col], infer_datetime_format=True)
            except (ValueError, FileNotFoundError, TypeError) as error:
                check_path = os.path.isdir(brr_old_f)
                if (str(error) != "Invalid file path or buffer object type: <class 'NoneType'>") and (check_path == False) and (str(error) != "cannot unpack non-iterable NoneType object"):
                    if (str(error)) == "Missing column provided to 'parse_dates': 'DateTime'":
                        brr_old = read_pd_csv(brr_old_f, low_memory=False, index_col=[
                                              0], parse_dates=[0], infer_datetime_format=True)
                        brr_old = idx_to_dt(brr_old)
                    else:
                        print(error)
                else:
                    print("No file. Download aborted.")
                    ans1 = [None, None]
                    return ans1
            brr_old.head()
            brr_old.name = 'BRR'

        if (symbols == None) or ('BRTI' in symbols):

            if interval == '1m':
                print("")
                print("Searching:", brti_1m_dir)
                try:
                    brti_1m_old_f = get_recent(
                        dir=brti_1m_dir, file_type='csv', horizon=hzn)
                except ValueError as error:
                    if str(error) == "Invalid file path or buffer object type: <class 'NoneType'>":
                        print("Download aborted.")
                        ans1 = [None, None]
                        return ans1
                try:
                    brti_old_1m = read_pd_csv(brti_1m_old_f, low_memory=False, index_col=[
                                              index_col], parse_dates=[index_col], infer_datetime_format=True)
                except (ValueError, FileNotFoundError, TypeError) as error:
                    check_path = os.path.isdir(brr_old_f)
                    if (str(error) != "Invalid file path or buffer object type: <class 'NoneType'>") and (check_path == False) and (str(error) != "cannot unpack non-iterable NoneType object"):
                        if (str(error)) == "Missing column provided to 'parse_dates': 'DateTime'":
                            brti_old_1m = read_pd_csv(brti_1m_old_f, low_memory=False, index_col=[
                                                      0], parse_dates=[0], infer_datetime_format=True)
                            brti_old_1m = idx_to_dt(brti_old_1m)
                        else:
                            print(error)
                            return
                    else:
                        print("No file. Download aborted.")
                        ans1 = [None, None]
                        return ans1
                brti_old_1m.name = 'BRTI_1M'

            if (interval == '1h') or (resample == True) or (hzn == 'any'):
                print("")
                print("Searching:", brti_1h_dir)
                try:
                    brti_1h_old_f = get_recent(
                        dir=brti_1h_dir, file_type='csv', horizon=hzn)
                except ValueError as error:
                    if str(error) == "Invalid file path or buffer object type: <class 'NoneType'>":
                        print("Download aborted.")
                        ans1 = [None, None]
                        return ans1
                try:
                    brti_old_1h = read_pd_csv(brti_1h_old_f, low_memory=False, index_col=[
                                              index_col], parse_dates=[index_col], infer_datetime_format=True)
                except (ValueError, FileNotFoundError, TypeError) as error:
                    check_path = os.path.isdir(brr_old_f)
                    if (str(error) != "Invalid file path or buffer object type: <class 'NoneType'>") and (check_path == False) and (str(error) != "cannot unpack non-iterable NoneType object"):
                        if (str(error)) == "Missing column provided to 'parse_dates': 'DateTime'":
                            brti_old_1h = read_pd_csv(brti_1h_old_f, low_memory=False, index_col=[
                                                      0], parse_dates=[0], infer_datetime_format=True)
                            brti_old_1h = idx_to_dt(brti_old_1h)
                        else:
                            print(error)
                            return
                    else:
                        print("No file. Download aborted.")
                        ans1 = [None, None]
                        return ans1
                brti_old_1h.name = 'BRTI_1H'

        if hzn == 'any':
            if ('BRR' in symbols) and ('BRTI' in symbols):
                brr = brr_old
                brti_1h = brti_old_1h
                return brr, brti_1h
            elif 'BRR' in symbols:
                brr = brr_old
                brti_1h = None
                return brr, brti_1h
            elif 'BRTI' in symbols:
                brr = None
                brti_1h = brti_old_1h
                return brr, brti_1h

        else:
            cme_df = download_cme(username, password, path='./data/', folder=f'{dir}/full_datasets', limit=limit, dataset=dataset,
                                  processes=processes)

            if 'BRR' in symbols:
                brr_new = extract_cme_df(cme_df, 'BRR', folder=brr_dir)
            if 'BRTI' in symbols:
                brti_new = extract_cme_df(cme_df, 'BRTI', folder=brti_1m_dir)

            if (interval == '1h') and (hzn != 'any'):
                resample == True

            if resample == True:
                if 'BRTI' in symbols:
                    brti_1h_new = brti_new['BRTI'].resample('1H').ohlc()
                    brti_1h_new.index = pd.DatetimeIndex(brti_1h_new.index)
                    brti_1h_new.sort_index(ascending=True, inplace=True)
                    brti_1h_new.index.names = ['DateTime']
                    brti_1h_new.rename(
                        columns={'mdEntryPx': 'BRTI'}, inplace=True)
                    brti_1h_new.columns = brti_1h_new.columns.str.strip().str.capitalize(
                    ).str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

            if limit >= 2:
                if 'BRR' in symbols:
                    brr = concat_non_dupe_idx(brr_old, brr_new)
                if 'BRTI' in symbols:
                    if interval == '1m':
                        brti_1m = concat_non_dupe_idx(brti_old_1m, brti_new)
                    if 'brti_1h_new' in locals():
                        brti_1h = concat_non_dupe_idx(brti_old_1h, brti_1h_new)
            elif limit == 1:
                raise NotImplementedError(
                    "Setting limit to 1 will erroneously append metadata to the file. Set limit>=2.")

            # Save files:
            if 'brr' in locals():
                print("")
                if brr.equals(brr_old) == False:
                    brr_f_path = new_cme_fpath(brr, dataset='BRR', dir=brr_dir)
                    pd_to_csv(brr, brr_f_path, folder=brr_dir)
                    print("")
                else:
                    print("No new updates to BRR")

            if 'brti_1m' in locals():
                print("")
                if brti_1m.equals(brti_old_1m) == False:
                    brti_1m_f_path = new_cme_fpath(
                        brti_1m, dataset='BRTI_1M', dir=brti_1m_dir)
                    pd_to_csv(brti_1m, brti_1m_f_path, folder=brti_1m_dir)
                    print("")
                else:
                    print("No new updates to BRTI 1M")

            if 'brti_1h' in locals():
                print("")
                if brti_1h.equals(brti_old_1h) == False:
                    brti_1h_f_path = new_cme_fpath(
                        brti_1h, dataset='BRTI_1H', dir=brti_1h_dir)
                    pd_to_csv(brti_1h, brti_1h_f_path, folder=brti_1h_dir)
                    print("")
                else:
                    print("No new updates to BRTI 1H")

            if ('brr' in locals()) and ('brti_1h' in locals()):
                return brr, brti_1h
            elif 'brr' in locals():
                return brr
            elif 'brti_1h' in locals():
                return brti_1h
