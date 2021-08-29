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
from pwe.pwetools import to_csv,get_recent,append_non_duplicates

import datamine.io as dm
from pprint import pprint as pp

def download_cme(username, password, path='./data2/', folder='csv_files', limit=2,dataset='CRYPTOCURRENCY',processes=1):
    """
    Establish an object to interact with CME Datamine.
    Supply Credentials per Documentation: http://www.cmegroup.com/market-data/datamine-api.html
    Params:
    processes: The pulls are multithreaded to speed them up; you can adjust this by adjusting the processes in the MyDatamine object.
    folder:  The name of the local directory for saving CSV files. Ensure that it is reserved only for CME data. 
            Do not maually alter the csv file names. The file names are read to determine the most recent csv.
    """
    myDatamine = dm.DatamineCon(username=username, password=password, path=path)

    myDatamine.get_catalog(dataset=dataset, limit=limit)
    myDatamine.data_catalog.popitem()

    dataCatalogDF = pd.DataFrame.from_dict(myDatamine.data_catalog,).T
    dataCatalogDF.dataset.value_counts()
    dataCatalogDF

    myDatamine.processes = processes
    if dataset=='CRYPTOCURRENCY':
        myDatamine.crypto_load(download=False)
        myDatamine.crypto_DF.index = pd.to_datetime(myDatamine.crypto_DF.index)
        myDatamine.crypto_DF.symbol.value_counts()
        cme_df = myDatamine.crypto_DF
        cme_df.index = pd.DatetimeIndex(cme_df.index)

        new_cme_f_name = new_cme_fpath(dataset='CRYPTOCURRENCY')
        to_csv(df=cme_df, folder=folder,f_name=new_cme_f_name)
    
    return cme_df;

def new_cme_fpath(cme_df, dataset='CRYPTOCURRENCY', dir='csv_files/CME/Crypto'):
    """
    Check the dates and times of the CME dataframe and format the file name accordingly.
    """
    cme_start = cme_df.index.min()
    print (cme_start)
    cme_end = cme_df.index.max()
    print (cme_end)

    cme_fdate_start = cme_start.strftime('%Y-%m-%d')
    cme_fdate_end = cme_end.strftime('%Y-%m-%d')
    
    cme_f_date = None

    if (cme_fdate_start == cme_fdate_end) and (cme_end -cme_start) == timedelta(hours=23, minutes=59, seconds=59):

        cme_f_date= cme_fdate_end
        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_f_date}.csv'

    elif (cme_fdate_start != cme_fdate_end) and ((str(cme_start.time()) == "00:00:00") and (str(cme_end.time()) == "23:59:59")):

        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_fdate_start}_{cme_fdate_end}.csv'

    elif (cme_fdate_start != cme_fdate_end) and ((str(cme_start.time()) != "00:00:00") or (str(cme_end.time()) != "23:59:59")):
        cme_fdt_start= cme_start.strftime('%Y-%m-%d,%M,%H,%S,%Z')
        cme_fdt_end = cme_end.strftime('%Y-%m-%d,%M,%H,%S,%Z')
        new_cme_f_name = f'./{dir}/CME_{dataset}_{cme_fdt_start}_{cme_fdt_end}.csv'
    else:
        raise ValueError("Date format issue.")

    return new_cme_f_name;

def extract_cme_df(cme_df, symbol):
    """
    Extract the relevent security into dataframe.
    symbol  : (str) - the relevent ticker. e.g. "BRR" , "BRTI".
    """
    df = pd.DataFrame(cme_df.loc[cme_df['symbol'] ==symbol,'mdEntryPx'])

    df.rename(columns={'mdEntryPx': f'{symbol}'},inplace=True)
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    df.index=pd.DatetimeIndex(df.index)
    df.sort_index(ascending=True, inplace=True)
    df.index.names = ['DateTime']

    return df;


def get_cme(username, password, dataset='CRYPTOCURRENCY',horizon='yesterday', dir='csv_files/CME/Crypto', index_col='DateTime', limit=2,
processes=1, resample=True):
    """
    Establish an object to interact with CME Datamine.
    Supply Credentials per Documentation: http://www.cmegroup.com/market-data/datamine-api.html
    Download CME Datamine data, import it into a project in a padas dataframe and save it to csv.
    If the data already exists locally, combine the new data with the most recent existing csv.
    If no new data exists, and a local file exists, import from local file.
    Params:
    dataset : The desired dataset, as per CME Datamine API name.
    limit : the number of most recent items to downnload. Default is 2 (metadata item and the most recet day of data.)
    path : the ame of local directory for savig the unformatted JSON data.
    processes: The pulls are multithreaded to speed them up; you can adjust this by adjusting the processes in the MyDatamine object.
    horizon : the acceptable timeframe for existing local data. If 'today', if no local file exists today, it will download new data.
    """
    if dataset=='CRYPTOCURRENCY':

        brr_dir = f"{dir}/BRR"
        brr_old_f = get_recent(dir=brr_dir,file_type='csv', horizon=horizon)
        brr_old = pd.read_csv(brr_old_f,low_memory=False, index_col=[index_col], parse_dates=[index_col],infer_datetime_format=True)
        brr_old.name = 'BRR'

        brti_1m_dir = f"{dir}/BRTI/1m"
        brti_1m_old_f = get_recent(dir=brti_1m_dir,file_type='csv', horizon=horizon)
        brti_old_1m = pd.read_csv(brti_1m_old_f,low_memory=False, index_col=[index_col], parse_dates=[index_col],infer_datetime_format=True)
        brti_old_1m.name = 'BRTI_1M'

        cme_df = download_cme(username, password, path='./data/', folder='csv_files/CME/Crypto/full_datasets', limit=limit,dataset=dataset,
        processes=processes)

        brr_new = extract_cme_df(cme_df, 'BRR')
        brti_new = extract_cme_df(cme_df, 'BRTI')

        if resample==True:
            brti_1h_dir = f"{dir}/BRTI/1h"
            brti_1h_old_f = get_recent(dir=brti_1h_dir,file_type='csv', horizon=horizon)
            brti_old_1h = pd.read_csv(brti_1h_old_f,low_memory=False, index_col=[index_col], parse_dates=[index_col],infer_datetime_format=True)
            brti_old_1h.name = 'BRTI_1H'

            brti_1h_new = brti_new['BRTI'].resample('1H').ohlc()
            brti_1h_new.index=pd.DatetimeIndex(brti_1h_new.index)
            brti_1h_new.sort_index(ascending=True, inplace=True)
            brti_1h_new.index.names = ['DateTime']
            brti_1h_new.rename(columns={'mdEntryPx': 'BRTI'},inplace=True)
            brti_1h_new.columns = brti_1h_new.columns.str.strip().str.capitalize().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

        if limit==2:
            brr = pd.concat([brr_old, brr_new])
            brti_1m = pd.concat([brti_old_1m, brti_new])
            brti_1h = pd.concat([brti_old_1h, brti_1h_new])
        elif limit>2:
            brr = append_non_duplicates(brr_old, brr_new, col=None)
            brti_1m = append_non_duplicates(brti_old_1m, brti_new, col=None)
            brti_1h = append_non_duplicates(brti_old_1h, brti_1h_new, col=None)
        elif limit==1:
            raise NotImplementedError("Setting limit to 1 will erroneously append metadata to the file. Set limit>=2.")

        # Save files:
        brr_f_path = new_cme_fpath(brr, dataset='BRR', dir=brr_dir)
        brti_1m_f_path = new_cme_fpath(brti_1m, dataset='BRTI_1H', dir=brti_1m_dir)
        brti_1h_f_path = new_cme_fpath(brti_1h, dataset='BRR', dir=brti_1h_dir)

        brr.to_csv(brr_f_path)
        print (f"saved csv to {brr_f_path}")

        brti_1m.to_csv(brti_1m_f_path)
        print (f"saved csv to {brti_1m_f_path}")

        brti_1h.to_csv(brti_1h_f_path)
        print (f"saved csv to {brti_1h_f_path}")

        return brr, brti_1h
