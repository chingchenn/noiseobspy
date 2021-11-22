# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 21:49:27 2020

@author: grace
"""


import glob
import pandas as pd
import datetime as dt
import matplotlib as mpl
from obspy import UTCDateTime
from pandas.core.frame import DataFrame

#把所有的單天newcsv整理成一個all.csv
# DIR='D:/2020summer/池上/TEMPETURE/daydata/'
DIR='D:/2020summer/RAINFALL/'
newtemp=pd.DataFrame()
newdate=pd.DataFrame()
newhpa=pd.DataFrame()
newprep=pd.DataFrame()
newwind=pd.DataFrame()

for k,file in enumerate(sorted(glob.glob(DIR+'*'+'new.csv'))):
    print(file)
    df = pd.read_csv(file,sep=',',header = None)
    dfnnew = df.drop(index=[0,1])
    
    UTClist = dfnnew[1]
    temp = dfnnew[2]
    hpa = dfnnew[3]
    prep = dfnnew[4]
    wind = dfnnew[5]
    UTCff = pd.Series(UTClist) 
    ddd = DataFrame(UTClist) 
    ttt = DataFrame(temp) 
    hhh = DataFrame(hpa) 
    ppp = DataFrame(prep)
    www = DataFrame(wind) 
    newdate = pd.concat([newdate,ddd],axis = 0)
    newtemp = pd.concat([newtemp,ttt],axis = 0)
    newhpa = pd.concat([newhpa,hhh],axis = 0)
    newprep = pd.concat([newprep,ppp],axis = 0)
    newwind = pd.concat([newwind,www],axis = 0)
    newccc=pd.concat([newdate,newtemp,newhpa,newprep,newwind],axis = 1)  
# newccc.to_csv(DIR+'all.csv',header = ['date-time','tempeture','hPa','rain prep','wind vel'])