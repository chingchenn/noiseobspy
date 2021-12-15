# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:24:52 2020

@author: grace
"""


import glob
import time
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl
from obspy import UTCDateTime
from pandas.core.frame import DataFrame

##還在失敗中##
DIR='D:/2020summer/池上/TEMPETURE/daydata/'
newtemp=pd.DataFrame()
newdate=pd.DataFrame()
newhpa=pd.DataFrame()
newprep=pd.DataFrame()
newwind=pd.DataFrame()

file =DIR+'all.csv'
print(file)
df = pd.read_csv(file,sep=',')
UTClist = df['date-time']
temp = df['tempeture']
hpa = df['hPa']
prep = df['rain prep']
wind = df['wind vel']
UTCttt = []
def strjjj(jjj):
    jjj=str(jjj)
    if len(jjj)==1:
        return '00'+jjj
    elif len(jjj)==2:
        return '0'+jjj
    else: return jjj
for ddd in UTClist:
    yyyy = ddd.rsplit('-',2)[0]
    month = ddd.rsplit('-',2)[1]
    day = ddd.rsplit('-',2)[2].rsplit(' ',2)[0]
    UTC=dt.datetime(year=int(yyyy), month=int(month), day=int(day))
    jjj = time.strptime(yyyy+'.'+month+'.'+day, "%Y.%m.%d").tm_yday
    n = str(yyyy)+'/'+str(jjj)
    UTCttt.append(n)
UTCttt = DataFrame(UTCttt)
outdf = pd.read_csv(file,sep = ',',usecols = [2,3,4,5])
testccc=pd.concat([UTCttt,outdf],axis = 1)
i = 0
iii = '2013/42'
# UTCttt = np.array(UTCttt)
# UTCttt = UTCttt.tolist()
date1 = dt.datetime(2012, 12, 31)
date2 = dt.datetime(2017, 1, 1)
delta= dt.timedelta(days=1)
dates= mpl.dates.drange(date1, date2, delta)
for a,uuu in enumerate(dates):
    UUU=UTCDateTime(mpl.dates.num2date(uuu))
    jjj=strjjj(UUU.julday)
    month = str(UUU.month)
    day = str(UUU.day)
    julday = UTCttt[a].rsplit('/',2)[1]
    if julday==jjj:
        print('f')
    # if df[a] == uuu:
        # print (testccc[0][a],temp[a])
        # print (iii)
        # temppp = []
        # temppp+=temp[a]
        

    
    # UTCff = pd.Series(UTClist) 
    # ddd = DataFrame(UTClist) 
    # ttt = DataFrame(temp) 
    # hhh = DataFrame(hpa) 
    # ppp = DataFrame(prep)
    # www = DataFrame(wind) 
    # newdate = pd.concat([newdate,ddd],axis = 0)
    # newtemp = pd.concat([newtemp,ttt],axis = 0)
    # newhpa = pd.concat([newhpa,hhh],axis = 0)
    # newprep = pd.concat([newprep,ppp],axis = 0)
    # newwind = pd.concat([newwind,www],axis = 0)
    # newccc=pd.concat([newdate,newtemp,newhpa,newprep,newwind],axis = 1)  
# newccc.to_csv(DIR+'all.csv',header = ['date-time','tempeture','hPa','rain prep','wind vel'])