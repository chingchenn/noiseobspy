#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:18:41 2020

@author: wtl_st
"""

import glob
import pandas as pd
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.core import UTCDateTime


fig, ax = plt.subplots(nrows=2,ncols=1,gridspec_kw={'height_ratios':[1,1]})
plt.rcParams['figure.figsize'] =35,9

bbbbyyyyyyy = 'CGF5days_4s_0.2'
pair='CHS5-CHS4'
freqmin=3
freqmax=6 
xmin=3
xmax=7
HZ = str(freqmin)+'_'+str(freqmax) 
window= str(xmin)+'_'+str(xmax)
csvpath='D:/2020summer/CHS/stretching/count/'+bbbbyyyyyyy+'/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'_nolevel.csv'
LIM = 0.2
time=dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2020, 1, 1, 0, 0)
df = pd.read_csv(glob.glob(csvpath)[0])
shift_n=df.dvv_n
shift_p=df.dvv_p
coeff_n=df.coeff_n
coeff_p=df.coeff_p
JJJ=list(df.juliday)


def strjjj(jjj):
    jjj=str(jjj)
    if len(jjj)==1:
        return '00'+jjj
    elif len(jjj)==2:
        return '0'+jjj
    else: return jjj
CGF_day_list=[]
for i , UTC in enumerate(JJJ):
    yyyy=UTC.rsplit('/',1)[0]
    jjj=UTC.rsplit('/',1)[1]
    aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
    UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
    CGF_day_list.append(UUU)
    
ax[0].axhline(y=0,color='lightgrey')
aaa=ax[0].scatter(CGF_day_list,shift_p,c=coeff_p,cmap='rainbow',lw=1,vmin=0.0, vmax=1.0)
ax[0].set_ylabel('positive dv/v',fontsize=20)
ax[0].set_xlim(time)
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
ax[0].grid(axis='x')
ax[0].set_xticklabels(labels=[],fontsize=15)
ax[0].tick_params(which='major', length=12,labelsize=20)
ax[0].set_title(pair+'  w='+window+'  hz='+HZ+'  date:'+'   '+bbbbyyyyyyy,fontsize=22,fontweight='bold')
ax[0].set_ylim(LIM,-LIM)
# ax[0].text(dt.datetime(2013, 1, 30, 0, 0),0.14,'Negative',fontsize=30,bbox=dict(facecolor='pink', alpha=0.7))
ax[0].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
ax[0].tick_params(which='minor', length=10,labelsize=20)

ax[1].axhline(y=0,color='lightgrey')
ax[1].scatter(CGF_day_list,shift_n,c=coeff_n,cmap='rainbow',lw=1,vmin=0.0, vmax=1.0)      
ax[1].set_ylabel('negative dv/v',fontsize=20)
# ax[1].set_xlabel('UTC',fontsize=20)
ax[1].set_xlim(time)
# ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
ax[1].grid(axis='x')
ax[1].tick_params(which='major', length=12,labelsize=20)
ax[1].set_ylim(LIM,-LIM)
# ax[1].text(dt.datetime(2013, 1, 30, 0, 0),0.14,'Positive',fontsize=30,bbox=dict(facecolor='pink', alpha=0.7))
ax[1].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
ax[1].tick_params(which='minor', length=10,labelsize=20)
plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
cax = plt.axes([0.8, 0.1, 0.01, 0.81])
cbr=fig.colorbar(aaa, cax=cax)
cbr.set_label('Coefficient',fontsize=22)

# fig.savefig( 'D:/TGA/CHS/2013-2019'+'/'+pair+'_'+window+'_'+HZ+'.jpg')



