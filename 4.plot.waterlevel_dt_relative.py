# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 01:10:09 2020

@author: grace
"""
from pylab import *
import pandas as pd
import datetime as dt
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib.dates as mdates
from obspy.core import UTCDateTime
from matplotlib.dates import (YEARLY, DateFormatter,date2num,num2date,
                              rrulewrapper, RRuleLocator, drange)
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


#讀_out.csv的檔案
plt.rcParams['figure.figsize'] =15,15

pair='CHS5-CHS4'
window='3_7'
YEAR='2013-2016'
stkdays=5
HZ = '3_6'
LIM = 0.2
filename = 'D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'_out.csv'
df=pd.read_csv(glob.glob(filename)[0])
dt_n=df.dvv_n
dt_p=df.dvv_p
coef_n=df.coeff_n
coef_p=df.coeff_p
level=df.waterlevel
jday_n=df.juliday
yfu_n = df.yfunction_n
yfu_p = df.yfunction_p
##=====================================================
cccn,p =  pearsonr(level, dt_n)
cccp,p = pearsonr(level, dt_p)

print(cccn,cccp)
##=====================================================
ax = subplot(221)
aaa=plt.scatter(level,dt_n,lw=0.5,c=coef_n,cmap='rainbow',vmin=0.0, vmax=1)
plt.plot(level,yfu_n,'k',lw = 3)
plt.ylim(-LIM,LIM)
plt.xlim(253,272)
plt.ylabel('dv/v ',fontsize=20)
plt.xlabel('Groundwater level (m)',fontsize=20)
plt.text(255,LIM*0.8,'Negative',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
plt.text(255,LIM*0.68,'the ccc number='+str(round(cccn,3)),fontsize=14)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(2))

plt.subplot(222)
plt.subplots_adjust(wspace=0.12) 
plt.scatter(level,dt_p,lw=0.5,c=coef_p,cmap='rainbow',vmin=0.0, vmax=1)
plt.plot(level,yfu_p,'k',lw = 3)
plt.ylim(-LIM,LIM)
plt.xlim(253,272)
plt.ylabel('dv/v',fontsize=20)
plt.xlabel('Groundwater level (m)',fontsize=20)
plt.text(267,LIM*0.8,'Positive',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
plt.text(262,LIM*0.68,'the ccc number='+str(round(cccp,3)),fontsize=14)
plt.xticks(fontsize=15)
plt.yticks([])
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(2))
plt.suptitle(pair+'\n  w='+window+'  hz='+HZ+'  date:'+YEAR,fontsize=22,fontweight='bold')
plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
cax = plt.axes([0.81, 0.5, 0.02, 0.41])
cbr=plt.colorbar(aaa, cax=cax)
cbr.set_label('Coefficient',fontsize=22)      
# plt.savefig( 'D:/TGA/0918'+'/'+pair+'_'+YEAR+'_'+window+'  '+HZ+'_dt_waterrelationship.jpg')
