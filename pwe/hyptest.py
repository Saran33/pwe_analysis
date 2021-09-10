#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:00:18 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
from collections import OrderedDict
#from scipy.stats import ttest_1samp, ttest_ind, shapiro, mannwhitneyu, f_oneway, chi2_contingency
from scipy.stats import ttest_ind, ttest_1samp, wilcoxon

def which_mean_test():
    """
    Accepts user input to suggest an appropriate significance test for making an interence about a mean.
    A simple decision tree for deciding which test to use.
    The approporiate scipy function and paramaters are returned to the user.
    It may be expanded upon to include other tests, to execute tests progromatically or to itegrate with machine learning models.
    """
    # binomtest
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html#scipy.stats.binomtest
    # hypergeom
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html
    # mannwhitneyu
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    # wilcoxon
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html

    test = None
    trim = None
    equal_var = False
    
    er_y_or_n = 'Invalid Input. Please enter "Y" or "N" or "yes" or "no"'
    er_1_or_2 = 'Invalid Input. Please enter "1" or "2"'

    n_dist = None

    try:
        print ("Is the sample size greater than 30? Y/N?")
        over_30 = str(input())

        if over_30.lower() in ('y','yes'):
            
            print ("")
            print ("Is the population normally distributed? Y/N?")
            n_dist = str(input())

            if n_dist.lower() in ('y','yes'):
                print ("")
                print ("Are the samples independent? Y/N?")
                ind = str(input())

                if ind.lower() in ('n','no'):
                    type = 't'
                
                elif ind.lower() in ('y','yes'):
                    
                    print ("")
                    print ("Is the data randomly selected from a population? Y/N?")
                    rndm = str(input())

                    if rndm.lower() in ('n','no'):
                        type = 't'

                    elif rndm.lower() in ('y','yes'):
                        
                        print ("")
                        print ("Are the two samples sets of the same size? Y/N?")
                        eql_size = str(input())

                        if eql_size.lower() in ('n','no'):
                            type = 't'
                        elif eql_size.lower() in ('y','yes'):
                            type = 'z'
                        else:
                            print(er_y_or_n)
                            print ("")
                            return which_mean_test()
                    else:
                        print(er_y_or_n)
                        print ("")
                        return which_mean_test()
                else:
                    print(er_y_or_n)
                    print ("")
                    return which_mean_test()

            elif n_dist.lower() in ('n','no'):
                print ("")
                print("Is the population variance known?")
                pop_var = str(input())

                if pop_var.lower() in ('y','yes'):

                    print ("")
                    print ("Are the samples independent? Y/N?")
                    ind = str(input())

                    if ind.lower() in ('n','no'):
                        type = 't'
                    
                    elif ind.lower() in ('y','yes'):
                        print ("")
                        print("Consider a Z test.") 
                        type = 'z'  

                elif pop_var.lower() in ('n','no'):
                    
                    print ("")
                    print ("Is the population large? Y/N?")
                    large = str(input())

                    if large.lower() in ('y','yes'):
                        print ("")
                        print("Consider a binomial test.") 
                        test = 'binomtest'
                        return test;
                    
                    elif large.lower() in ('n','no'):
                        print ("")
                        print("Consider a hypergeometric test.") 
                        test = 'hypergeom'
                        return test;
                    else:
                        print(er_y_or_n)
                        print ("")
                        return which_mean_test()
                else:
                    print(er_y_or_n)
                    print ("")
                    return which_mean_test()
            else:
                print(er_y_or_n)
                print ("")
                return which_mean_test()

        elif over_30.lower() in ('n','no'):
            print ("")
            print("Is the population variance known?")
            pop_var = str(input())

            if pop_var.lower() in ('y','yes'):
                print ("")
                print("Consider a Z test.") 
                type = 'z'

            elif pop_var.lower() in ('n','no'):
                type = 't'
            else:
                print(er_y_or_n)
                print ("")
                return which_mean_test()
        else:
            print(er_y_or_n)
            print ("")
            return which_mean_test()

        ##############################################################
        # Z-tests:
        ##############################################################
        if type == 'z':    

            print ("")    
            print ("Are you: \n\n1. Comparing one group of independent observations to the population? \n\nOR:")
            print ("\n2. Comparing two related or repeated samples of scores? 1 or 2?")
            samp = int(input())
            
            if samp == 1:
                test = "stests.ztest"
                print ("")
                print ("One-sample Z-test")
                print ("from statsmodels.stats import weightstats as stests")
                print (test)
                
            elif samp == 2:
                test = "stests.ztest"
                print ("")
                print ("Two-sample Z-test")
                print ("from statsmodels.stats import weightstats as stests")
                print (test)
            else:
                print(er_1_or_2)
                print ("")
                return which_mean_test()
                
            #print (f"{test}")
            return test;

        ##############################################################
        # t-tests:
        ##############################################################
        elif type == 't':

            print ("")
            print ("Are the two samples from the same group or related? Y/N?")
            same = str(input())
            
            if same.lower() in ('y','yes'):
                
                print ("")
                print ("Are you: \n\n1. Comparing one group of independent observations to the population? \n\nOR:")
                print ("\n2. Comparing two related or repeated samples of scores? 1 or 2?")
                samp = int(input())
                
                if samp == 1:
                    test = "ttest_1samp"
                    print ("")
                    print ("One Sample t-test")
                    print (test)
                    print ("https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html")
                    
                elif samp == 2:
                    test = "ttest_rel"
                    print ("Dependent (Paired) t-test")
                    print (test)
                else:
                    print(er_1_or_2)
                    print ("")
                    return which_mean_test()
            
            elif same.lower() in ('n','no'):
                
                print ("")
                print ("Are the two samples sets of the same size? Y/N?")
                eq_size = str(input())

                if eq_size.lower() in ('y','yes'):
                    var = None
                
                elif eq_size.lower() in ('n','no'):
                    print ("")
                    print ("Do the two samples have the same variance? Y/N?")
                    var = str(input())

                    if var.lower() not in ('n','no','y','yes'):
                        print(er_y_or_n)
                        print ("")
                        return which_mean_test()
                else:
                    print(er_y_or_n)
                    print ("")
                    return which_mean_test()
                
                if n_dist == None:
                    print ("")
                    print("Are the distributions long-tailed or contaminated with outliers? Y/N?")
                    tails = str(input())

                    if tails.lower() in ('y','yes'):
                        n_dist = 'n'

                    elif tails.lower() in ('n','no'):
                        n_dist = 'y'
                    else:
                        print(er_y_or_n)
                        print ("")
                        return which_mean_test()
                    print ("")
                
                if var != None:
                    if (eq_size.lower() in ('n','no')) & (var.lower() in ('n','no')) & (n_dist.lower() in ('n','no')):
                        test = "ttest_ind"
                        equal_var = False
                        trim = True
                        print ("")
                        print ("Yuen-Welch’s t-test")
            
                    elif (eq_size.lower() in ('n','no')) & (var.lower() in ('n','no')) & (n_dist.lower() in ('y','yes')):
                        test = "ttest_ind"
                        equal_var = False
                        print ("")
                        print ("Unequal Variance (Welch’s) t-test")
                        
                    elif (n_dist.lower() in ('n','no')):
                        test = "ttest_ind"
                        equal_var = True
                        trim = True
                        print ("")
                        print ("Yuen's t-test (trimmed mean)")
                        
                    elif (var.lower() in ('y','yes')) & (n_dist.lower() in ('y','yes')):
                        test = "ttest_ind"
                        equal_var = True
                        print ("")
                        print ("Equal Variance (Independent) t-test")
                    else: 
                        print(er_y_or_n)
                        print ("")
                        return which_mean_test()

                if test ==None:
                    if (n_dist==None):
                        print ("")
                        print ("Is the population normally distributed? Y/N?")
                        n_dist = str(input())

                        if n_dist.lower() not in ('n','no','y','yes'):
                            print(er_y_or_n)
                            print ("")
                            return which_mean_test()

                    if (n_dist.lower() in ('n','no')):
                        test = "ttest_ind"
                        equal_var = True
                        trim = True
                        print ("")
                        print ("Yuen's t-test (trimmed mean)")
                    
                    elif (n_dist.lower() in ('y','yes')):
                        test = "ttest_ind"
                        equal_var = True
                        print ("")
                        print ("Equal Variance (Independent) t-test")                                 
                    else: 
                        print(er_y_or_n)
                        print ("")
                        return which_mean_test()
                
            print (f"{test}(equal_var={equal_var}, trim={trim})")
            return test, equal_var, trim
    
    except Exception as error:
        print(er_y_or_n)
        print (error)
        print ("")
        return which_mean_test()

def ttest_ind_(group1, group2, H_1='two-sided', median=False, 
                group1_name=None, group2_name=None, nan_policy='omit',
                permutations=None, random_state=None, equal_var=True, trim=0):
    """
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html

    H_1         : alternative {‘two-sided’, ‘less’, ‘greater’}

    For H_1='two-sided':
            H_0: the mean of Group1 is no different to the mean of Group2.
            H_1: the mean of Group1 significantly differs to the mean of Group2. 

    For H_1='less':
            H_0: the mean of Group1 is greater than or equal to the mean of Group2.
            H_1: the mean of Group1 is statistically significantly less than the mean of Group2.
            
    For H_1='greater':
            H_0: the mean of Group1 is less than or equal to the mean of Group2.
            H_1: the mean of Group1 is statistically significantly greater than the mean of Group2.
    
    """
    if group1_name ==None:
        group1_name = 'Group 1'
    if group2_name ==None:
        group2_name = 'Group 2'
    
    print(f"{group1_name} Size:",group1.count())
    print(f"{group1_name} Nan values:",group1.isnull().sum())
    print("")
    print(f"{group2_name} Size:",group2.count())
    print(f"{group2_name} Nan Values:",group2.isnull().sum())
    print("")
    
    if median:
        group1_med = group1.median()
        group2_med = group2.median() 
    else:
        group1_med = group1.mean()
        group2_med = group2.mean()
    
    print(f"Mean {group1_name} returns:", "{:.6%}".format(group1_med))
    print (f"Mean {group2_name} returns:", "{:.6%}".format(group2_med))
    print("")
    if group1_med<group2_med:
        diff = "{:.2%}".format(abs((group2_med-group1_med)/group2_med))
        print (f"The mean of {group1_name} is {diff} lower than the mean of {group2_name}.")
    if group1_med>group2_med:
        diff = "{:.2%}".format(abs((group1_med-group2_med)/group2_med))
        print (f"The mean of {group1_name} is {diff} higher than the mean of {group2_name}.")
    print("")
    
    group1_std = group1.std()
    group2_std = group2.std()
    print(f"{group1_name} returns σ:", "{:.6%}".format(group1_std))
    print (f"{group2_name} returns σ:", "{:.6%}".format(group2_std))
    print("")
    
    tstat,pval = ttest_ind(group1,group2,nan_policy=nan_policy,alternative=H_1,trim=trim,
                    permutations=permutations,random_state=random_state,equal_var=equal_var)
    
    print('p-value:',"{:.6}".format(pval))
    print('t-stat:',"{:.6}".format(tstat))

    if H_1=='two-sided':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    elif H_1=='less' or H_1=='greater':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    return pval;

def ttest_1samp_(sample, pop, H_1='less', sample_name=None, pop_name=None, nan_policy='omit',):
    """
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html

    scipy.stats.ttest_1samp(a, popmean, axis=0, nan_policy='propagate', alternative='two-sided')

    H_1         : alternative {‘two-sided’, ‘less’, ‘greater’}

    For H_1='two-sided':
            H_0: the sample mean is no different to the pop mean.
            H_1: the sample mean is statistically different to the pop mean.

    For H_1='less':
            H_0: the sample mean is greater than or equal to the pop mean.
            H_1: the sample mean is statistically significantly less than the pop mean.
            
    For H_1='greater':
            H_0: the sample mean is less than or equal to the pop mean.
            H_1: the sample mean is statistically significantly greater than the pop mean.
    
    """
    if sample_name ==None:
        sample_name = 'Sample'
    if pop_name ==None:
        pop_name = 'Population'

    print(f"{sample_name} Size:",sample.count())
    print(f"{sample_name} Nan values: ",sample.isnull().sum())
    print("")
    print(f"{pop_name} Size:",pop.count())
    print(f"{pop_name} Nan Values: ",pop.isnull().sum())
    print("")

    sample_mean = sample.mean()
    pop_mean = pop.mean()
    print(f"Mean {sample_name} returns:", "{:.6%}".format(sample_mean))
    print (f"Mean {pop_name} returns:", "{:.6%}".format(pop_mean))
    print("")
    if sample_mean<pop_mean:
        diff = "{:,.3%}".format(abs((pop_mean-sample_mean)/pop_mean))
        ab_ret  = "{:,.2%}".format(-1*abs(((pop_mean-sample_mean)/pop_mean)))
        print (f"Returns are {diff} lower than average.")
        print (ab_ret)
    if sample_mean>pop_mean:
        diff = "{:,.3%}".format(abs((sample_mean-pop_mean)/pop_mean))
        ab_ret  = "{:,.2%}".format(abs((sample_mean-pop_mean)/pop_mean))
        print (f"Returns are {diff} higher than average.")
        print (ab_ret)
    print("")
    
    sample_std = sample.std()
    pop_std = pop.std()
    print(f"{sample_name} returns σ:", "{:.6%}".format(sample_std))
    print (f"{pop_name} returns σ:", "{:.6%}".format(pop_std))
    print("")
    
    tstat,pval = ttest_1samp(sample, pop_mean, nan_policy=nan_policy,alternative=H_1)
    print('p-value:',"{:.6}".format(pval))
    print('t-stat:',"{:.6}".format(tstat))

    if H_1=='two-sided':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    elif H_1=='less' or H_1=='greater':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    return pval, ab_ret;

from scipy.stats  import wilcoxon, mannwhitneyu, ranksums

def wilcoxon_sr(group1, group2, H_1='two-sided', 
                group1_name=None, group2_name=None,
                zero_method='wilcox',correction=False,mode='auto'):
    """
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html
    """
    if group1_name ==None:
        group1_name = 'Group 1'
    if group2_name ==None:
        group2_name = 'Group 2'
    
    print(f"{group1_name} Size:",group1.count())
    print(f"{group1_name} Nan values:",group1.isnull().sum())
    print("")
    print(f"{group2_name} Size:",group2.count())
    print(f"{group2_name} Nan Values:",group2.isnull().sum())
    print("")
    
    group1_med = group1.median()
    group2_med = group2.median() 
    
    print(f"Median {group1_name} returns:", "{:.6%}".format(group1_med))
    print (f"Median {group2_name} returns:", "{:.6%}".format(group2_med))
    print("")
    if group1_med<group2_med:
        diff = "{:.2%}".format(abs((group2_med-group1_med)/group2_med))
        print (f"The median of {group1_name} is {diff} lower than the mean of {group2_name}.")
    if group1_med>group2_med:
        diff = "{:.2%}".format(abs((group1_med-group2_med)/group2_med))
        print (f"The median of {group1_name} is {diff} higher than the mean of {group2_name}.")
    print("")
    
    group1_std = group1.std()
    group2_std = group2.std()
    print(f"{group1_name} returns σ:", "{:.6%}".format(group1_std))
    print (f"{group2_name} returns σ:", "{:.6%}".format(group2_std))
    print("")
    
    if group1.count() == group2.count():
        w , pval = wilcoxon(group1, group2, zero_method=zero_method, correction=correction, alternative=H_1, mode=mode)
    else:
        w , pval = wilcoxon(group1-group2_med, zero_method=zero_method, correction=correction, alternative=H_1, mode=mode)
    
    print('p-value:',"{:.6}".format(pval))
    print('w-stat:',"{:.6}".format(w))

    if H_1=='two-sided':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    elif H_1=='less' or H_1=='greater':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    return pval;

def man_whitney_u(group1, group2, H_1='two-sided', group1_name=None, group2_name=None,
                    use_continuity=True, axis=0, method='auto'):
    """
    Mann-Whitney U rank test 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html#scipy.stats.mannwhitneyu
    """
    if group1_name ==None:
        group1_name = 'Group 1'
    if group2_name ==None:
        group2_name = 'Group 2'
    
    print(f"{group1_name} Size:",group1.count())
    print(f"{group1_name} Nan values:",group1.isnull().sum())
    print("")
    print(f"{group2_name} Size:",group2.count())
    print(f"{group2_name} Nan Values:",group2.isnull().sum())
    print("")
    
    group1_med = group1.median()
    group2_med = group2.median() 
    
    print(f"Median {group1_name} returns:", "{:.6%}".format(group1_med))
    print (f"Median {group2_name} returns:", "{:.6%}".format(group2_med))
    print("")
    if group1_med<group2_med:
        diff = "{:.2%}".format(abs((group2_med-group1_med)/group2_med))
        print (f"The median of {group1_name} is {diff} lower than the mean of {group2_name}.")
    if group1_med>group2_med:
        diff = "{:.2%}".format(abs((group1_med-group2_med)/group2_med))
        print (f"The median of {group1_name} is {diff} higher than the mean of {group2_name}.")
    print("")
    
    group1_std = group1.std()
    group2_std = group2.std()
    print(f"{group1_name} returns σ:", "{:.6%}".format(group1_std))
    print (f"{group2_name} returns σ:", "{:.6%}".format(group2_std))
    print("")
    
    u, pval = mannwhitneyu(group1.dropna(), group2.dropna(), use_continuity=use_continuity, alternative=H_1, axis=axis, method=method)
    
    print('p-value:',"{:.6}".format(pval))
    print('w-stat:',"{:.6}".format(u))

    if H_1=='two-sided':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    elif H_1=='less' or H_1=='greater':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    return pval;

def w_ranksums(group1, group2, H_1='two-sided', group1_name=None, group2_name=None):
    """
    This test should be used to compare two samples from continuous distributions. 
    It does not handle ties between measurements in x and y.
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ranksums.html
    Accepts nans.
    """
    if group1_name ==None:
        group1_name = 'Group 1'
    if group2_name ==None:
        group2_name = 'Group 2'
    
    print(f"{group1_name} Size:",group1.count())
    print(f"{group1_name} Nan values:",group1.isnull().sum())
    print("")
    print(f"{group2_name} Size:",group2.count())
    print(f"{group2_name} Nan Values:",group2.isnull().sum())
    print("")
    
    group1_med = group1.median()
    group2_med = group2.median() 
    
    print(f"Median {group1_name} returns:", "{:.6%}".format(group1_med))
    print (f"Median {group2_name} returns:", "{:.6%}".format(group2_med))
    print("")
    if group1_med<group2_med:
        diff = "{:.2%}".format(abs((group2_med-group1_med)/group2_med))
        print (f"The median of {group1_name} is {diff} lower than the mean of {group2_name}.")
    if group1_med>group2_med:
        diff = "{:.2%}".format(abs((group1_med-group2_med)/group2_med))
        print (f"The median of {group1_name} is {diff} higher than the mean of {group2_name}.")
    print("")
    
    group1_std = group1.std()
    group2_std = group2.std()
    print(f"{group1_name} returns σ:", "{:.6%}".format(group1_std))
    print (f"{group2_name} returns σ:", "{:.6%}".format(group2_std))
    print("")
    
    rs, pval = ranksums(group1, group2, alternative=H_1)
    
    print('p-value:',"{:.6}".format(pval))
    print('w-stat:',"{:.6}".format(rs))

    if H_1=='two-sided':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    elif H_1=='less' or H_1=='greater':
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")

    return pval;
    
def pval_table(prefix_strs, series_names=['2018/01/01-2021/09/01', '2019/09/01-2021/09/01'], interval='Hourly', p_decimals=2, ret_decimals=6):
    """
    A specific function for manipulating numerous securiies into a dataframe of stats. Needs to be copied and pasted for 'eval' to work.
    Including it here for reference, despite the fact it is not generalizable.
    Bit of a hack. Needs to be pasted into a notebook for (eval) to work for python globals.
    """
    df_dict = OrderedDict()
    for prefix_str, series_name in zip(prefix_strs,series_names):
        table_df = pd.DataFrame()
        delta_lst =[]
        suffix_str_lst = ['_min72_48','_less48','_min48_24', '_less24','_t_min_0','_plus24', '_plus24_48','_plus48_72']
        for suffix_str in suffix_str_lst:
            delta_lst.append("{pref}{suff}".format(pref=prefix_str,suff=suffix_str))

        delta_dict = OrderedDict()
        series_name_lst = []
        for item in delta_lst:
            sec = eval(item)
            if sec.name!=item:
                setattr(sec, 'name', item)
            delta_dict[item] = sec

        series_name_lst = ['T-72 to T-48','T-48 to T-0', 'T-48 to T-24', 'T-24 to T-0', 'T-0', 'T-0 to T+24', 'T+24 to T+48', 'T+48 to T+72']
        table_df['Timedelta'] = series_name_lst
        table_df[f'{series_name} key'] = delta_lst

        ret_dict = OrderedDict()
        for key in delta_dict.keys():
            ret_dict[key] = delta_dict[key].avg_ret
        table_df[f'Mean {interval} Return'] = pd.Series([round(val, 6) for val in ret_dict.values()], index = table_df.index)
        table_df[f'Mean {interval} Return'] = pd.Series([f"{val*100:.{ret_decimals}f}%" for val in table_df[f'Mean {interval} Return']], index = table_df.index)

        ret_dict = OrderedDict()
        for key in delta_dict.keys():
            ret_dict[key] = delta_dict[key].ab_ret
        table_df['Abnormal Return'] = pd.Series([val for val in ret_dict.values()], index = table_df.index)
        #table_df['Abnormal Return'] = pd.Series([f"{val*100:.{ret_decimals}f}%" for val in table_df['Abnormal Return']], index = table_df.index)

        pval_dict = OrderedDict()
        for key in delta_dict.keys():
            pval_dict[key] = delta_dict[key].pval
        table_df['P-value'] = pd.Series([round(val, 6) for val in pval_dict.values()], index = table_df.index)
        table_df['P-value'] = pd.Series([f"{val*100:.{p_decimals}f}%" for val in table_df['P-value']], index = table_df.index)
        #table_df[f'{series_name} Abnormal {interval} Return'] =

        df_dict[series_name] = table_df

        df_total = pd.concat([df_dict[df] for df in df_dict.keys()], axis=1, keys=[df for df in df_dict.keys()])

    return delta_lst, delta_dict, df_total;