#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:43:58 2020

@author: wtl_st
"""


import math
import numpy as np
import datetime as dt
from scipy import stats
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
from obspy import read, read_inventory,Trace

# date1 = dt.datetime(2013, 1, 1)
# date2 = dt.datetime(2013, 12, 31)
# delta= dt.timedelta(days=1)
# dates= mpl.dates.drange(date1, date2, delta)
###==========================================================
CCF_DIR='D:/2020summer/CHS/D03_CCF'
STK_DIR='D:/2020summer/CHS/D04_stk'

# pair_list = ['IT01-IT03','IT01-IT04','IT01-IT05','IT01-IT07','IT01-IT09','IT02-IT01','IT02-IT03','IT02-IT04','IT02-IT05','IT02-IT06','IT02-IT07','IT02-IT08','IT02-IT09','IT02-IT10',
             # 'IT03-IT04','IT03-IT05','IT03-IT07','IT03-IT09','IT04-IT05','IT04-IT07','IT06-IT01','IT06-IT01','IT06-IT03','IT06-IT05','IT06-IT07','IT06-IT08','IT06-IT09','IT06-IT10',
             # 'IT07-IT05','IT08-IT01','IT08-IT03','IT08-IT04','IT08-IT05','IT08-IT07','IT09-IT05','IT09-IT04','IT10-IT01','IT10-IT03','IT10-IT04','IT10-IT05','IT10-IT07','IT10-IT09']
pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']

freqmin=3
freqmax=6
#分成頻率1-4(1-10)頻率2-8(1-10)與頻率5-10(1-10)
xmax=6
xmin=3
for pair in pair_list:
    plt.rcParams['figure.figsize'] =12,5
    RCF=read(glob.glob(STK_DIR+'/'+pair+'*low*stk')[0])
    # RCF=read(glob.glob(STK_DIR+'/'+pair+'*.HHZ.stk')[0])
    RCF.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
    starttime=RCF[0].stats.starttime
    # RCF_win = RCF
    RCF_win=RCF.slice(starttime=starttime+200+xmin,endtime=starttime+200+xmax)
    RCF_data=RCF_win[0].data
    plus_test_ccf=0;SSS=0
    SSSlist=[];coeff_list=[]
    for i,ccf in enumerate(sorted(glob.glob(CCF_DIR+'/'+pair+'/*.CCF'))[0:100]):
        print(ccf)
        CCF=read(ccf)
        # CCF_win = read(ccf)
        CCF_win=CCF.slice(starttime=starttime+200+xmin,endtime=starttime+200+xmax)
        CCF_win.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
        CCFdata=CCF_win[0].data
        plus_test_ccf+=CCFdata
        SSS+=1
        print(SSS)
        stk_test_ccf=plus_test_ccf / SSS
        if math.isnan(plus_test_ccf[-1]) == True:
            continue
        coeff,p=stats.pearsonr(RCF_data,stk_test_ccf)
        coeff=abs(coeff)
        coeff_list.append(coeff)
        SSSlist.append(SSS)
    if SSSlist == []:
        continue
    plt.scatter(SSSlist,coeff_list)
    plt.axhline(0.8,0,50,c='r')
    plt.title(pair+' stack v.s.'+'win= '+str(xmin)+'_'+str(xmax)+'  freq= '+str(freqmin)+'_'+str(freqmax))
    plt.savefig( 'D:/2020summer/CHS/'+pair+'_win='+str(xmin)+'_'+str(xmax)+'_freq='+str(freqmin)+'_'+str(freqmax)+'stk.jpg')
    print('----CCF_coeff'+pair+'win= '+str(xmin)+'_'+str(xmax)+'  freq= '+str(freqmin)+'_'+str(freqmax)+'stk.jpg Save-------')
    plt.clf()
    plt.show()    