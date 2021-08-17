#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:00:18 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp, ttest_ind, shapiro, mannwhitneyu, f_oneway, chi2_contingency

def returns_ttest(group1, group2, group1_stats, group2_stats, returns='Price_Returns',H_1='less', tails=1,
                  median=False,group1_name='Group1',group2_name='Group2'):
    """
    For H_1='less':
            H_0: the mean return of Group1 is greater than or equal to the average return of Group2.
            H_1: the mean return of Group1 hour is less than the average return of Group2.
            
    For H_1='greater':
            H_0: the mean return of Group1 is less than or equal to the average return of Group2.
            H_1: the mean return of Group1 is greater than the average return of Group2.
    
    """
    from scipy.stats import ttest_ind
    
    group1_returns = group1[returns]
    group2_returns = group2[returns]
    
    print(f"{group1_name} Size:",group1_returns.count())
    print(f"{group1_name} Nan values: ",group1_returns.isna().value_counts())
    print("")
    print(f"{group2_name} Size:",group2_returns.count())
    print(f"{group2_name} Nan Values: ",group2_returns.isna().value_counts())
    print("")
    
    if median==True:
        group1_mean = group1_stats.med_ret
        group2_mean = group2_stats.med_ret
        
    else:
        group1_mean = group1_stats.avg_ret
        group2_mean = group2_stats.avg_ret
    
    print(f"Mean {group1_name} returns:", group1_mean)
    print (f"Mean {group2_name} returns:", group2_mean)
    print("")
    
    group1_std = group1_stats.std_ret
    group2_std = group2_stats.std_ret
    print(f"{group1_name} returns σ:", group1_std)
    print (f"{group2_name} returns σ:", group2_std)
    print("")
    
    ttest,pval = ttest_ind(group1_returns,group2_returns,nan_policy='omit')
    
    if tails == 1:
        
        if H_1=='less':
            print("p-value:",pval)
        elif H_1=='greater':
            pval = 1-pval
            print("p-value:",pval)
        
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")
            
    elif tails == 2:
        
        if H_1=='less':
            one_tailed_p = pval/2
            print("p-value:",one_tailed_p)
        elif H_1=='greater':
            one_tailed_p = 1-pval/2
            print("p-value:",one_tailed_p)
        
        if one_tailed_p <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    return;