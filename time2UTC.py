# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 21:57:18 2020

@author: grace
"""

import glob
import pandas as pd
import datetime as dt
import matplotlib as mpl
from obspy import UTCDateTime
from pandas.core.frame import DataFrame

#把台灣時間換成UTC時間

DIR='D:/2020summer/池上/TEMPETURE/daydata'
date1 = dt.datetime(2014, 12, 30)
date2 = dt.datetime(2017, 1, 1)
delta= dt.timedelta(days=1)
dates= mpl.dates.drange(date1, date2, delta)
def strjjj(jjj):
    jjj=str(jjj)
    if len(jjj)==1:
        return '00'+jjj
    elif len(jjj)==2:
        return '0'+jjj
    else: return jjj
for UTC in dates:
    UUU=UTCDateTime(mpl.dates.num2date(UTC))
    jjj=strjjj(UUU.julday)
    month = str(UUU.month)
    day = str(UUU.day)
    if len(month) ==1:
        month = '0'+month
    if len(day) ==1:
        day = '0'+day
    for file in sorted(glob.glob(DIR+'*'+str(UUU.year)+'-'+month+'-'+day+'.csv')):
        df = pd.read_csv(file,sep=',')
        UTClist = ['Time']
        hour = df['觀測時間(hour)']
        temp = df['氣溫(℃)']
        hpa = df['測站氣壓(hPa)']
        wind = df['風速(m/s)']
        rain = df['降水量(mm)']
        for i in range (len(hour)-1):
            if int(hour[i+1])>=8:
                UTCll=dt.datetime(UUU.year,int(month),int(day),int(hour[i+1])-8,0,0)
                UTClist.append(UTCll)
            elif int(hour[i+1])<8:
                if int(month) <10 and int(day) == 1 and int(month) !=1:#2-9月每個月1號
                    month = '0'+str(UUU.month-1)
                    year = str(UUU.year)
                    if int(month) == 1 or int(month) ==3 or int(month) ==5 or int(month) ==7 or int(month) ==8:
                        day = str(31)
                        print('02,01 04,01 06,01 08,01 09,01')
                    elif int(month) == 4 or int(month) ==6:
                        day = str(30)
                        print('05,01 07,01')
                    elif int(month) == 2 :
                        day = str(28)
                        print('03,01')
                elif int(month) ==1 and int(day) == 1:#1月1號
                    month = str(12)
                    day = str(31)
                    year = str(UUU.year-1)
                    print('01,01')
                elif len(month) ==2 and len(str(UUU.day)) == 1 and day == '01':#10-12月每個月1號
                    if int(month) == 10:#10/1
                        month = '09'
                        day = str(30)
                        print('10,01')
                    elif int(month)==11:#11/1
                        month = '10'
                        day = '31'
                        print('11,01')
                    elif int(month)==12:#12/1
                        print('12,01')
                        month = '11'
                        day = '30'
                elif len(month) ==1 and len(day) == 1 and UUU.day != 1:#1-9月每個月2-9號
                    day = '0'+day
                    month = '0'+month
                    year = str(UUU.year)
                
                elif len(month) ==2 and len(day) == 1 and UUU.day != 1:#10-12月每個月2-9號
                    year = str(UUU.year)
                    month = month
                    day = '0'+day
                elif len(month) ==1 and len(day)==2:#1-9月每個月10~號
                    year = str(UUU.year)
                    month = '0'+month
                    day = day
                elif len(month)==2 and  len(day)==2:#10-12月每個月10~號
                    year = str(UUU.year)
                    month = month
                    day = day
                else:
                    print('============'+month,day+'=============')
                UTCll=dt.datetime(int(year),int(month),int(day)-1,int(hour[i+1])-8+24,0,0)
                UTClist.append(UTCll)
        UTCff = pd.Series(UTClist) 
        newtemp = pd.concat([UTCff,temp,hpa,rain,wind],axis = 1)
        newtemp.to_csv(DIR+str(UUU.year)+'-'+str(jjj)+'new.csv')
        #print(str(UUU.month)+'/'+str(UUU.day))
        print('--save--'+str(jjj))