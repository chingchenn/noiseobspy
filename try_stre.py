# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:00:08 2020

@author: grace
"""


import pandas as pd
import matplotlib.pyplot as plt
import sys, obspy, os,glob
import datetime as dt
import numpy as np
from obspy import read, read_inventory,Trace
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
from obspy.core import UTCDateTime
from matplotlib.dates import (YEARLY, DateFormatter,date2num,num2date,rrulewrapper, RRuleLocator, drange)

plt.rcParams['figure.figsize'] =15,9

pair='CHS5-CHS4'
window='2.5_5'
YEAR='2013-2016'
SAC_DIR= 'D:/2020summer/CHS/stretching/'


k=0.005
n=3
nn=0.3
m=0.003
col=['r','b','g','gray']
# for i,sta in enumerate(sorted(glob.glob(SAC_DIR+'CHS5-CHS4*292*.n.interp200'))):
for i,sta in enumerate(sorted(glob.glob(SAC_DIR+str(nn)+'_reference.p.interp200'))):
    dt=sta
    print(sta)
    st = read(sta)
    lags=np.arange(0,st[0].stats.npts)
    data =st[0].data
    for n in range(5):
        if n ==0:
            plt.plot(lags-m*(2)*10**3,data+n*k,c=col[i],lw=4)
        if n ==1:
            plt.plot(lags-m*(1)*10**3,data+n*k,c=col[i],lw=4)
        if n >2:
            plt.plot(lags+m*(n-1)*8**3,data+n*k,c=col[i],lw=4)
        if n ==2:
            plt.plot(lags,data+n*k,c=col[i],lw=4,label="RGF")



for RGF in sorted(glob.glob(SAC_DIR+'CHS5-CHS4.2018.125.HHZ.CGF.bp3-6.cut.3.7.p.interp200')):
    for j in range(n+1):

        st = read(RGF)
        lags=np.arange(0,st[0].stats.npts)
        data =st[0].data
        plt.plot(lags,data+j*k,'k',lw=4)
        if j ==4:
            plt.plot(lags,data+j*k,'k',lw=4,label="CGF")
# plt.legend(fontsize=28,loc = 'lower left')
# plt.legend(fontsize=30,loc = 4)
# plt.text(30,0.0296999,'dt/t',fontsize = 30)
# plt.text(52,-0.007,'2.85',fontsize = 25)
# plt.text(470,-0.007,'5.45',fontsize = 25)
plt.xticks([])
plt.xlim(50,650)
plt.yticks([])
plt.xlabel('Lags (s)',fontsize = 30)
ax = plt.gca()
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
# plt.savefig('/home/teach/Poster'+'/'+'stretched_dt'+'.pdf')