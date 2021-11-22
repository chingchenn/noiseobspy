# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:33:40 2020

@author: grace
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

CCF_DIR='D:/2020summer/CHS/D03_CCF'
STK_DIR='D:/2020summer/CHS/stretching/stk'
pair = 'CHS5-CHS3'
freqmin=1
freqmax=4
#分成頻率1-4(1-10)頻率2-8(1-10)與頻率5-10(1-10)
xmax=10
xmin=1

plt.rcParams['figure.figsize'] =24,10
RCF=read(glob.glob(STK_DIR+'/'+pair+'**stk')[0])
RCF.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
starttime=RCF[0].stats.starttime
RCF_win=RCF.slice(starttime=starttime+200+xmin,endtime=starttime+200+xmax)
RCF_data=RCF_win[0].data
plus_test_ccf=0;SSS=0
SSSlist=[];coeff_list=[]
for i,ccf in enumerate(sorted(glob.glob(CCF_DIR+'/'+pair+'/*.CCF'))[0:30]):
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
plt.scatter(SSSlist,coeff_list,c='g',s=100,marker='s')
plt.axhline(0.9,0,50,c='r')
plt.ylim(0.8,1)
plt.xlim(0,30)
ax = plt.gca()
ax.spines['bottom'].set_linewidth(5)
ax.spines['top'].set_linewidth(5)
ax.spines['left'].set_linewidth(5)
ax.spines['right'].set_linewidth(5)
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)
plt.title(pair+' stack v.s.'+'win= '+str(xmin)+'_'+str(xmax)+'  freq= '+str(freqmin)+'_'+str(freqmax),fontsize=35)
# plt.savefig( 'D:/2020summer/ITCH/'+pair+'_win='+str(xmin)+'_'+str(xmax)+'_freq='+str(freqmin)+'_'+str(freqmax)+'stk.jpg')
print('----CCF_coeff'+pair+'win= '+str(xmin)+'_'+str(xmax)+'  freq= '+str(freqmin)+'_'+str(freqmax)+'stk.jpg Save-------')
plt.show()    