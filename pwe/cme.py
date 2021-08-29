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
from pwe.pwetools import df_to_csv,get_recent

import datamine.io as dm
from pprint import pprint as pp

username='api_saranconnolly'
cme_api_key='#rt6JJ74%Qh#H6G@JG$%$6@E'

def download_cme(username=username, password=cme_api_key, path='./data2/', folder='csv_files', limit=2,dataset='CRYPTOCURRENCY',processes=1):
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
        df_to_csv(df=cme_df, folder=folder,f_name=new_cme_f_name)
    
    return cme_df;

def new_cme_fpath(cme_df, dataset='CRYPTOCURRENCY'):
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
        new_cme_f_name = f'./csv_files/CME_{dataset}_{cme_f_date}.csv'

    elif (cme_fdate_start != cme_fdate_end) and ((str(cme_start.time()) == "00:00:00") and (str(cme_end.time()) == "23:59:59")):

        new_cme_f_name = f'./csv_files/CME_{dataset}_{cme_fdate_start}_{cme_fdate_end}.csv'

    elif (cme_fdate_start != cme_fdate_end) and ((str(cme_start.time()) != "00:00:00") or (str(cme_end.time()) != "23:59:59")):
        cme_fdt_start= cme_start.strftime('%Y-%m-%d,%M,%H,%S,%Z')
        cme_fdt_end = cme_end.strftime('%Y-%m-%d,%M,%H,%S,%Z')
        new_cme_f_name = f'./csv_files/CME_{dataset}_{cme_fdt_start}_{cme_fdt_end}.csv'
    else:
        raise ValueError("Date format issue.")

    print (new_cme_f_name)
    return new_cme_f_name;


def get_cme(username=username, password=cme_api_key, path='./data2/', folder='csv_files', limit=2,dataset='CRYPTOCURRENCY',processes=1,
horizon='yesterday', dir='csv_files/CME/Crypto'):
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
    """
    latest_file = get_recent(dir=dir,file_type='csv', horizon=horizon)

    df = pd.read_csv(latest_file,low_memory=False, index_col=['DateTime'], parse_dates=['DateTime'],infer_datetime_format=True)
    df.name = dataset

    return df;

get_cme(username=username, password=cme_api_key, path='./data2/', folder='csv_files', limit=2,dataset='CRYPTOCURRENCY',processes=1,
horizon='yesterday', dir='csv_files/CME/Crypto')
 
