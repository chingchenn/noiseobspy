# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:47:30 2020

@author: grace
"""


#算出線性回歸的理論值，存到out.csv裡
import numpy as np
import scipy as sp
import pandas as pd
import datetime as dt
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.dates as mdates
from scipy.optimize import leastsq
from obspy.core import UTCDateTime1
from pandas.core.frame import DataFrame
from matplotlib.dates import (YEARLY, DateFormatter,date2num,num2date,
                              rrulewrapper, RRuleLocator, drange)
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
window_list = ['2_6','3_7','4_8','5_9','6_10','7_11','8_12']
HZ_list = ['1_4','3_6','5_8']
stkdays=5
pair_list = ['CHS5-CHS4']
window_list = ['2_6','3_7']
HZ_list = ['1_4','3_6']

for pair in pair_list:
    for window in window_list:
        for HZ in HZ_list:
            filename= 'D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'yyyy.csv'
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
            yp = k1*Xp+b1 #理論值
            yt_p = yp.tolist()
            Xn = np.array(level)
            Yn = np.array(dt_n)
            p0 = [10,10]
            Para = leastsq(error,p0,args=(Xn,Yn))
            k2,b2 = Para[0]
            yn = k2*Xn+b2 #理論值
            yt_n = yn.tolist()
            r_n = yt_n-dt_n #殘差
            r_p = yt_p-dt_p #殘差
            out=pd.DataFrame({'juliday':jday, 'waterlevel':level, 'dvv_n': dt_n,
                                'coeff_n': coef_n, 'yfunction_n':yt_n, 'residual_n':r_n,
                                'dvv_p':dt_p,
                                'coeff_p':coef_p,
                                'yfunction_p':yt_p,
                                'residual_p':r_p })
            out.to_csv('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'_out.csv')
            print('DONE for '+pair+'_'+window+'_bp'+HZ+'out.csv')
