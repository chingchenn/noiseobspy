# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 11:07:17 2020

@author: grace
"""


import glob
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl
from obspy import UTCDateTime
from pandas.core.frame import DataFrame

#把所有的單天newcsv整理成一個all.csv
# DIR='D:/2020summer/池上/TEMPETURE/monthdata/'
DIR='D:/2020summer/RAINFALL/'
newtemp=pd.DataFrame()
newdate=pd.DataFrame()
newhpa=pd.DataFrame()
newprep=pd.DataFrame()
newwind=pd.DataFrame()
newddd = []

for file in sorted(glob.glob(DIR+'/rainfall_670/*'+'.csv')):
    print(file)
    df = pd.read_csv(file,sep=',',usecols = [0,1,7,16,21])
    dfnnew = df.drop(index=[0])
    day = dfnnew['觀測時間(day)']
    hpa = dfnnew['測站氣壓(hPa)']
    temp = dfnnew['氣溫(℃)']
    wind = dfnnew['風速(m/s)']
    prep = dfnnew['降水量(mm)']
    mm=((file.rsplit('\\',2)[1]).rsplit('.',2)[0]).rsplit('-',3)[2]
    yyyy = ((file.rsplit('\\',2)[1]).rsplit('.',2)[0]).rsplit('-',3)[1]
    for i in range(len(day)):
        date = str(yyyy)+'-'+str(mm)+'-'+str(day[i+1])
        newddd.append(date)
        ttt = DataFrame(temp) 
        hhh = DataFrame(hpa) 
        ppp = DataFrame(prep)
        www = DataFrame(wind) 
        ddd = pd.Series(newddd) 
    
    newtemp = pd.concat([newtemp,ttt],axis = 0)
    newhpa = pd.concat([newhpa,hhh],axis = 0)
    newprep = pd.concat([newprep,ppp],axis = 0)
    newwind = pd.concat([newwind,www],axis = 0)
    newkkk=pd.concat([newtemp,newhpa,newprep,newwind],axis = 1)
newkk = np.array(newkkk)
nn = pd.DataFrame(newkk)
newdate = pd.concat([newdate,ddd],axis = 0)
newccc=pd.concat([newdate,nn],axis = 1)  
newccc.to_csv(DIR+'670.csv',header = ['date-time','tempeture','hPa','rain prep','wind vel'])