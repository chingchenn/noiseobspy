# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:23:01 2020

@author: grace
"""


import csv
import glob
import time
import math
import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats
import matplotlib as mpl
from obspy import UTCDateTime
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from CCF_functions import whiten,normalize
from matplotlib.dates import (YearLocator, MONTHLY,DateFormatter,AutoDateLocator)


# ###此程式還沒寫完，是用來做week的計算，還在考慮要不要寫???


plt.rcParams['figure.figsize'] =15,7
YEAR='2013-2016'
pair = 'CHS5-CHS3'
window ='4_8'
HZ = '1_4'

date1 = dt.datetime(2012, 12, 30)
date2 = dt.datetime(2015, 1, 1)
delta= dt.timedelta(days=1)
dates= mpl.dates.drange(date1, date2, delta)

tttdate = [];ttt = [];UTCttt = []
# file = 'D:/2020summer/池上/TEMPETURE/daydata/all.csv'
file = 'D:/2020summer/池上/TEMPETURE/monthdata/tt.csv'
df = pd.read_csv(file)
date = df['date-time']
tem = df['tempeture']
hPa = df['hPa']
prep = df['rain prep']
vel = df['wind vel']
for i in range (len(tem)):
    if tem[i]==str('...'):
        tem[i]=20
    if hPa[i]==str('...'):
        hPa[i] = 990
    if prep[i]==str('...'):
        prep[i]=0
    elif prep[i]==str('...') or prep[i]==str('/') :
        prep[i]=0  
    if vel[i]==str('...') or vel[i] ==str('X'):
        vel[i]=0
tem = list(map(float, tem))
hPa = list(map(float, hPa))
prep = list(map(float, prep))
vel = list(map(float, vel))
for UUU in date:
    year = UUU.rsplit('-',3)[0]
    month=UUU.rsplit('-',3)[1]
    day=UUU.rsplit('-',3)[2].rsplit(' ',2)[0]
    UTC=dt.datetime(year=int(year), month=int(month), day=int(day))
    jjj = time.strptime(year+'.'+month+'.'+day, "%Y.%m.%d").tm_yday
    UTCttt.append(UTC)
waterpath='D:/2020summer/池上/池上地下水.csv'
grounddate=[];groundwater=[];UTCground=[]
with open (waterpath,newline='') as wfile:
    rows=list(csv.reader(wfile,delimiter=','))
    for row in rows[1:]:
        grounddate.append(row[0])
        groundwater.append(float(row[1]))
    for UUU in grounddate:
        year=UUU.rsplit('/',3)[0]
        month=UUU.rsplit('/',3)[1]
        day=UUU.rsplit('/',3)[2]
        UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
        UTCground.append(UTC)

refile = 'D:/2020summer/CHS/stretching/count/CGF11days/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'out.csv'
# refile = 'D:/2020summer/CHS/stretching/count/CGF11days/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'outlier.csv'
df1 = pd.read_csv(refile)
# r_n = df1.residual_n
# r_p = df1.residual_p
# r_n = df1.dvv_n
# r_p = df1.dvv_p
r_n = df1.yfunction_n
r_p = df1.yfunction_p
r_n = list(map(float, r_n))
rn = []
r_p = list(map(float, r_p))
rp = []
JJJ=list(df1.juliday)
CGF_day_list=[]

for i , UTC in enumerate(JJJ):
    if type(UTC) ==float:
        break
    yyyy=UTC.rsplit('/',1)[0]
    jjj=UTC.rsplit('/',1)[1]
    aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
    UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
    CGF_day_list.append(UUU)
    rp.append(r_p[i])
    rn.append(r_n[i])

lista = []
listb = []
listc = []
listd = []
listp3 = []
listv3 = []
listv4 = []

m = np.mean(groundwater)
n = np.std(groundwater)
m1 = np.mean(tem)
n1 = np.std(tem)
h = np.mean(hPa)
e = np.std(hPa) 
p1 = np.mean(prep)
p2 = np.std(prep)
f = np.mean(rn)
q = np.std(rn)
s = np.mean(rp)
w = np.std(rp)

for i in range (len(groundwater)):
    a = (groundwater[i]-m)/n
    lista.append(a)
    b = (groundwater[i]-m)/n
    listb.append(b)
for i in range (len(tem)):
    a = (tem[i]-m1)/n1
    listv3.append(a)
    b = (hPa[i]-h)/e
    listv4.append(b)
    p3 = (prep[i]-p1)/p2
    listp3.append(p3)
    
for j in range(len(rn)):
    c = (rn[j]-f)/q
    listc.append(c)
for j in range(len(rp)):    
    d = (rp[j]-s)/w
    listd.append(d)



####====================雨量==========================
formatter = DateFormatter('20%y')
newrain=[]
newUTC=[]
path = 'D:/2020summer/CHS/Chihshang_prep_finish/'
for i,csvfile in enumerate(sorted(glob.glob(path+'*week.csv'))):
    sta = (csvfile.rsplit('/',4)[-1].rsplit('\\',2)[1]).rsplit('_',3)[0]
    df = pd.read_csv(csvfile, encoding= 'unicode_escape')
    date = np.array(df.Time).tolist()
    rain= np.array(df.Prep).tolist()
    
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
            
listrr = []
uu = np.mean(newrain)
uun = np.std(newrain)
for i in range(len(newrain)):
    r1 = (newrain[i]-uu)/uun
    listrr.append(abs(r1))    
    
    
    
########################   plot  2   window   ###############################   
fig, ax = plt.subplots(nrows=2,ncols=1,gridspec_kw={'height_ratios':[1,3]}) 
ax[0].bar(newUTC,listrr,width=10,color = 'gray')
# ax[0].bar(newUTC,newrain,width=10,color = 'gray')
# ax[0].set_yscale("log")
ax[0].set_xlim(dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2016, 12, 31, 0, 0))

# ax[1].scatter(UTCttt,listv3,c = 'r',lw = 0.3,ls='-',label = 'tempeture')
# ax[1].scatter(UTCttt,listv4,c = 'chocolate',label = 'hPa',s=1.5)
ax[1].scatter(CGF_day_list,listc,c = 'b',s = 5,label= "negative dvv")
# ax[1].scatter(CGF_day_list,listd,c = 'g',s = 5,label= "postive dvv")
ax[1].set_xlim(dt.datetime(2013, 3, 1, 0, 0),dt.datetime(2016, 12, 31, 0, 0)) 
ax[1].scatter(UTCground,lista,color = 'k',label= "groundwater",s=3)
# ax[1].set_ylim(-4,4)
ax[1].legend(fontsize=12)

 ########################   plot  1   window   ###############################      
# plt.xlim(dt.datetime(2013, 5, 1, 0, 0),dt.datetime(2017, 1, 1, 0, 0))
# plt.scatter(UTCground,lista,color = 'k',label= "groundwater",s=0.5)
# plt.scatter(CGF_day_list_n,listc,c = 'b',s = 7,ls='-',label= "negative dvv")
# plt.scatter(CGF_day_list_p,listd,c = 'g',s = 7,label= "postive dvv")
# # plt.scatter(UTCttt,listv3,color = 'r',label = 'tempeture',s=5)
# plt.scatter(UTCttt,listv4,color = 'chocolate',label = 'hPa',s=5)
# plt.ylim(-4,4)
# plt.legend(fontsize=12)
# # # plt.title()
# plt.show()

# crosscorr = np.correlate(listv4,listv3, mode='full')
# plt.plot(crosscorr)
# coeff1_n,p=stats.pearsonr(listv3,listv4)
# # # plt.text(-200,0,coeff1_n)
# plt.show()

