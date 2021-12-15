# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:38:00 2020

@author: grace
"""

import numpy as np
import sys, obspy, os,glob
from obspy import read, read_inventory,Trace
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
from obspy.geodetics import locations2degrees
import matplotlib as mpl
import pandas as pd
import datetime as dt
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY,YearLocator, MONTHLY,DateFormatter,
                              rrulewrapper, RRuleLocator, drange,AutoDateLocator)
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
plt.rcParams['figure.figsize'] =30,12
# fig, ax = plt.subplots(nrows=3,ncols=1,gridspec_kw={'height_ratios':[1,2]})
fig, ax = plt.subplots(nrows=3,ncols=1)    
#==============================================================================
waterpath='D:/2020summer/池上/Chihshang_groundwater_level_2013-2016.csv'
grounddate=[];groundwater=[];UTCground=[]
with open (waterpath,newline='') as wfile:
    rows=list(csv.reader(wfile,delimiter=','))
    for row in rows[1:]:
        grounddate.append(row[1])
        groundwater.append(float(row[2]))
    for UUU in grounddate:
        year=UUU.rsplit('/',3)[0]
        month=UUU.rsplit('/',3)[1]
        day=UUU.rsplit('/',3)[2]
        UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
        UTCground.append(UTC)
ax2 = ax[0].twinx()
ax2.plot(UTCground,groundwater,c='blue',lw=5,ls='-')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.set_ylabel('Groundwater5 elevation (m)',c='blue',fontsize=20)
pair='CHS5-CHS2'
window='2_5'
YEAR='2013-2016'
HZ = '1_4'
FIG_DIR='/home/wtl_st/Poster/stretching'
csvpath = 'D:/2020summer/summer2020/stretching/count/new/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'w.csv'
df = pd.read_csv(glob.glob(csvpath)[0])
shift_n=df.shift_n
shift_p=df.shift_p
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
    
ax[1].axhline(y=0,color='lightgrey')
aaa=ax[1].scatter(CGF_day_list,shift_n,c=coeff_n,cmap='Reds',lw=1,vmin=0.4, vmax=1)
ax[1].set_ylabel('Shift time (s)',fontsize=20)
ax[1].set_xlim(dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2017, 1, 1, 0, 0))
# ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
ax[1].grid(axis='x')
ax[1].set_xticklabels(labels=[],fontsize=15)
ax[1].tick_params(which='major', length=12,labelsize=20)
ax[1].set_title(pair+'  w='+window+'  hz='+HZ+'  date:'+YEAR,fontsize=22,fontweight='bold')
ax[1].set_ylim(-0.06,0.06)
# ax[0].text(dt.datetime(2013, 1, 30, 0, 0),0.14,'Negative',fontsize=30,bbox=dict(facecolor='pink', alpha=0.7))
ax[1].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
ax[1].tick_params(which='minor', length=10,labelsize=20)
# ax2.xaxis.set_major_locator(ticker.MultipleLocator(3.00))


#==============================================================================

formatter = DateFormatter('20%y')
newrain=[]
newUTC=[]
for i,csvfile in enumerate(sorted(glob.glob(path+'\\*阿里山.csv'))):
    sta = (csvfile.rsplit('\\',2)[2]).rsplit('.',2)[0]
    print(sta)
    stanum=sta.rsplit('_',2)[0]
    df = pd.read_csv(csvfile, header= 0, encoding= 'unicode_escape')
    date = np.array(df.date).tolist()
    rain= np.array(df.prep).tolist()
    
    for r in rain:
        if r == str('T')  :
            r = 0
        elif r==str("...") :
            r = 0
        elif r ==str('X'):
            r = 0
        newrain.append(float(r))
    for U in date:
        yyyy1=int(str(U)[0:4])
        mm1=int(str(U)[4:6])
        dd1=int(str(U)[6:8])

        date3=UTCDateTime(year=yyyy1,month=mm1,day=dd1)
        UTC1=dt.datetime(year=date3.year, month=date3.month, day=date3.day,fold=1)

        newUTC.append(UTC1)
            
            
ax[0].plot(newUTC,newrain,c='k',markersize=0.5,marker='o')

ax[0].set_xlim(newUTC[0],newUTC[-1])
# plt.xlabel('Year',fontsize=17)
ax[0].set_ylabel('Precipitation (mm)\n',fontsize=17)
#ax[0].set_xticklabels(labels=[],fontsize=15)
#ax[0].set_xticklabels(labels=[],fontsize=15)
ax[0].tick_params(axis='both',labelsize=15)
ax[0].set_yscale("log")

locator = YearLocator()
ax[0].xaxis.set_major_locator(locator)
ax[0].xaxis.set_major_formatter(formatter)
ax[0].tick_params(which='major', length=7)
minloc = AutoDateLocator()
minloc.intervald[MONTHLY] = [6]
ax[0].xaxis.set_minor_locator(minloc)


#==============================================================================

pair='CHS4-CHS2'
CCF_DIR="D:/2020summer/summer2020/D03_CCF"
bbb=10**-1.5
xmin=2
xmax=5
lags=np.arange(-8000,8000)
freqmin=1
freqmax=4
file1=sorted(glob.glob(CCF_DIR+'/'+pair+'/*CCF'))[0]
yyyy1=file1.rsplit('.',5)[1]
jul1=file1.rsplit('.',5)[2]
UTC1=UTCDateTime(year=int(yyyy1),julday=int(jul1), hour=00, minute=0)
file2=sorted(glob.glob(CCF_DIR+'/'+pair+'/*CCF'))[-2]
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
    if int(yyyy)<=2016:
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
        ax[1].fill_betweenx(lags/40 ,data+y2, y2 ,where=data+y2<y2,lw=1.5,color='lightskyblue', alpha=0.7)
        ax[1].fill_betweenx(lags/40 ,data+y2, y2 ,where=data+y2>y2,lw=1.5,color='violet', alpha=0.7)
        ax[1].plot(data+y2,lags/40,'grey',lw=0.5)
        
        if a%50 ==0:
            ax[1].text(y2,xmax+0.09,jjj,fontsize=15)
        elif int(yyyy) != int(oldyyyy):
            ax[1].text(y2,xmax+0.24,yyyy,fontsize=18)
        oldyyyy=yyyy
    
ax[2].set_ylabel('Lags (s)',fontsize=20)
ax[2].set_xlabel('\n\nJulian Day',fontsize=20)
ax[2].set_xticks([])
ax[2].tick_params(axis='y',labelsize=15)
# ax[1].set_xlim(0,y2)
ax[2].set_ylim(xmax,xmin)
ax[2].set_title(pair+'bp'+str(freqmin)+'-'+str(freqmax)+'Hz',fontsize=20)
# fig.suptitle(pair,fontsize=25,fontweight='bold')

# plt.savefig(FIG_DIR+'/'+pair+'_'+yyyy+'_CCF_bp2-8_lag'+str(xmin)+str(xmax)+'.pdf')
# print('-------Figure Save-------')
# plt.close()
