# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:54:43 2020

@author: grace
"""
import csv
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
from obspy import read, read_inventory,Trace
from obspy.geodetics import locations2degrees
from matplotlib.dates import (YEARLY,YearLocator, MONTHLY,DateFormatter,
                              rrulewrapper, RRuleLocator, drange,AutoDateLocator)
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

pair='CHS5-CHS2'
YEAR='2013-2016'
freqmin=3
freqmax=6   
xmin=2
xmax=5
HZ = str(freqmin)+'_'+str(freqmax) 
window= str(xmin)+'_'+str(xmax)

CCF_DIR="D:/2020summer/summer2020/D03_CCF"
bbb=10**-1.5
lags=np.arange((200+xmin)*40,(200+xmax)*40)
file1=sorted(glob.glob(CCF_DIR+'/'+pair+'/*2013.07?.HHZ.CCF'))[0]
yyyy1=file1.rsplit('.',5)[1]
jul1=file1.rsplit('.',5)[2]
UTC1=UTCDateTime(year=int(yyyy1),julday=int(jul1), hour=00, minute=0)
file2=sorted(glob.glob(CCF_DIR+'/'+pair+'/*2013.07?.HHZ.CCF'))[-1]
yyyy2=file2.rsplit('.',5)[1]
jul2=file2.rsplit('.',5)[2]
UTC2=UTCDateTime(year=int(yyyy2),julday=int(jul2), hour=00, minute=0)

date1 = dt.datetime(UTC1.year, UTC1.month, UTC1.day)
date2 = dt.datetime(UTC2.year, UTC2.month, UTC2.day)
delta= dt.timedelta(days=1)
dates= mpl.dates.drange(date1, date2, delta)

oldyyyy=0
for a,UTC in enumerate(dates):
    UUU=UTCDateTime(mpl.dates.num2date(UTC))
    yyyy=str(UUU.year)
    y2=1.5*a*bbb
    if int(yyyy)<=2016 and int(yyyy)>=2013:
        jjj=str(UUU.julday)
        if len(jjj)==1:
            jjj='00'+jjj
        elif len(jjj)==2:
            jjj='0'+jjj
        else: jjj=jjj
        
        if sorted(glob.glob(CCF_DIR+'/'+pair+'/*'+yyyy+'.'+jjj+'*CCF'))==[]:
            continue
        msdpath=sorted(glob.glob(CCF_DIR+'/'+pair+'/*'+yyyy+'.'+jjj+'*CCF'))[0]
        print(msdpath)
        st=read(msdpath)  
        st.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
        data=st[0].data
        data_new = data[(200+xmin)*40:(200+xmax)*40]
        
        plt.fill_betweenx(lags/40 ,data_new+y2,y2,where=data_new+y2<y2,lw=1.5,color='lightskyblue', alpha=0.7)
        plt.fill_betweenx(lags/40 ,data_new+y2,y2,where=data_new+y2>y2,lw=1.5,color='violet', alpha=0.7)
        plt.plot(data_new+y2,lags/40,'grey',lw=0.5)
        
        # if int(jjj)%50 ==1:
            # plt.text(y2,xmax+0.1,jjj,fontsize= 12)
        # elif int(yyyy) != int(oldyyyy):
            # plt.text(y2-0.01,xmax+0.2,yyyy,fontsize=18)
            # oldyyyy=yyyy
    
plt.ylabel('Lags (s)',fontsize=20)
plt.xlabel('\n\nJulian Day',fontsize=20)
plt.xticks([])
plt.tick_params(axis='y',labelsize=15)
# plt.ylim(xmax,xmin)
plt.title(pair+'bp'+str(freqmin)+'-'+str(freqmax)+'Hz',fontsize=20)

