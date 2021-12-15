# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 22:40:22 2020

@author: grace
"""

#算出線性回歸的理論值，存到out.csv裡
import numpy as np
import scipy as sp
import pandas as pd
import datetime as dt
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import leastsq
from obspy.core import UTCDateTime
from pandas.core.frame import DataFrame
from matplotlib.dates import (YEARLY, DateFormatter,date2num,num2date,
                              rrulewrapper, RRuleLocator, drange)
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
plt.rcParams['figure.figsize'] =15,13
pair='CHS5-CHS2'
window='2_6'
YEAR='2013-2016'
stkdays=5
HZ = '3_6'
filename= 'D:/2020summer/CHS/stretching/count/CGF5days_4s/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'.csv'
df=pd.read_csv(glob.glob(filename)[0])
dt_n=df.dvv_n
dt_p=df.dvv_p
coef_n=df.coeff_n
coef_p=df.coeff_p
level=df.waterlevel
jday = df.juliday


Xp = np.array(level)
Yp = np.array(dt_p)
def func(p,x):
    k,b = p
    return k*x+b
def error(p,x,y):
    return func(p,x)-y
p0 = [10,10]
Para = leastsq(error,p0,args=(Xp,Yp))
k1,b1 = Para[0]
yp = k1*Xp+b1
yt_p = yp.tolist()
plt.scatter(Xp,Yp)


Xn = np.array(level)
Yn = np.array(dt_n)
p0 = [10,10]
Para = leastsq(error,p0,args=(Xn,Yn))
k1,b1 = Para[0]
yn = k1*Xn+b1
yt_n = yn.tolist()
plt.scatter(Xn,Yn)
plt.ylim(-0.04,0.04)
plt.title(pair+'  w = '+window+'  Hz = '+ HZ +' date:'+YEAR)
out=pd.DataFrame({'juliday':jday,
                  'waterlevel':level,
                    'dvv_n': dt_n,
                    'coeff_n': coef_n,
                    'yfunction_n':yt_n,
                    'dvv_p':dt_p,
                    'coeff_p':coef_p,
                    'yfunction_p':yt_p })
# out.to_csv('D:/2020summer/CHS/stretching/count/CGF5days_4s/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'out.csv')
file = 'D:/2020summer/CHS/stretching/count/CGF5days_4s/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'out.csv'
df1=pd.read_csv(glob.glob(file)[0])
yn= df1.yfunction_n
yp= df1.yfunction_p
dt_n=df1.dvv_n
dt_p=df1.dvv_p

plt.plot(level,yn,color = 'k',lw = 2)
plt.plot(level,yp,'--',color = 'k',lw = 1)