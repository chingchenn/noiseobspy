#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:58:31 2020

@author: teach
"""

from pylab import *
import pandas as pd
import datetime as dt
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.core import UTCDateTime
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib.dates import (YEARLY, DateFormatter,date2num,num2date,
                              rrulewrapper, RRuleLocator, drange)

plt.rcParams['figure.figsize'] =15,15

pair='CHS5-CHS4'
window='2_6'
YEAR='2013-2016'
stkdays=5
HZ = '3_6'
LIM = 0.2
filename = 'D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2_2013/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'_outlier.csv'
df=pd.read_csv(glob.glob(filename)[0])
dt_n=df.dvv_n
dt_p=df.dvv_p
coef_n=df.coeff_n
coef_p=df.coeff_p
level_n=df.waterlevel_n
level_p=df.waterlevel_p
jday_n=df.juliday_n
jday_p=df.juliday_p
yfu_n = df.yfunction_n
yfu_p = df.yfunction_p

ax = subplot(221)
aaa=plt.scatter(level_n,dt_n,lw=0.5,c=coef_n,cmap='rainbow',vmin=0.0, vmax=1)
plt.plot(dt_n,yfu_n,'k',lw = 3)
plt.ylim(-LIM,LIM)
plt.xlim(253,272)
plt.xlabel('dv/v ',fontsize=20)
plt.ylabel('Groundwater level (m)',fontsize=20)
# plt.text(-0.09,271,'Negative',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(2))

plt.subplot(222)
plt.subplots_adjust(wspace=0.12) 
plt.scatter(level_p,dt_p,lw=0.5,c=coef_p,cmap='rainbow',vmin=0.0, vmax=1)
plt.plot(-dt_p,yfu_p,'k',lw = 3)
plt.ylim(-LIM,LIM)
plt.xlim(253,272)
plt.xlabel('dv/v',fontsize=20)
# plt.text(0.05,271,'Positive',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
plt.xticks(fontsize=15)
plt.yticks([])
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(2))

plt.suptitle(pair+'\n'+YEAR+' stk '+str(stkdays)+' days'+'  w='+window,fontsize=20)

plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
cax = plt.axes([0.81, 0.5, 0.02, 0.41])
cbr=plt.colorbar(aaa, cax=cax)
cbr.set_label('Coefficient',fontsize=22)      

k2 =       -71.649665120193546
b2 = 257.85838668743656
# plt.text()
print('y=' +str(k2)+'*x+'+str(b2))

# plt.savefig('/home/teach/Poster/'+pair+'_'+'w'+window+'_stretching_dt_waterrelationship_5days_v3.pdf')