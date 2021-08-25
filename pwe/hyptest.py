#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 09:00:18 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import pandas as pd
import numpy as np
#from scipy.stats import ttest_1samp, ttest_ind, shapiro, mannwhitneyu, f_oneway, chi2_contingency
from scipy.stats import ttest_ind

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
    
    group1_std = group1_stats.vol
    group2_std = group2_stats.vol
    print(f"{group1_name} returns σ:", group1_std)
    print (f"{group2_name} returns σ:", group2_std)
    print("")
    
    ttest,pval = ttest_ind(group1_returns,group2_returns,nan_policy='omit')
    
    if tails == 2:
        
        if H_1=='less':
            print("p-value:",pval)
        elif H_1=='greater':
            pval = 1-pval
            print("p-value:",pval)
        
        if pval <0.05:
            print("We reject null hypothesis.")
        else:
            print("We fail to reject null hypothesis.")
            
    elif tails == 1:
        
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