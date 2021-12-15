# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 09:21:24 2020

@author: grace
"""

import math
import scipy
import numpy as np
import pandas as pd
from plot_mwcs import *
import numpy.fft as fft
from scipy import signal
import sys, obspy, os,glob
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from scipy.optimize import leastsq
from obspy.core.stream import Stream
from obspy import read, read_inventory,Trace
from numpy.fft import ifft, fftshift,fftfreq
from sklearn.linear_model import LinearRegression


plt.rcParams['figure.figsize']=10,7.5
SAC_DIR= 'D:/2020summer/CHS/stretching/'
CGF='D:/2020summer/CHS/stretching/02_CHS5-CHS4_CGF5days/CHS5-CHS4.2014.322.HHZ.CGF'
RGF='D:/2020summer/CHS/D04_stk/CHS5-CHS4.HHZ.stk'
freqmin=1
freqmax=4
endwin=20
startwin=2
CGF = read(CGF)
RGF = read(RGF)
lags=np.arange(-8000,8000)

plot_data_wave = 0
if plot_data_wave:
    plot_data(lags/40,RGF[0].data,CGF[0].data,startwin,endwin)
CGF.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
RGF.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)


# 選取時間段_拿整段coda!!!(正時間)
qqq=CGF.slice(starttime=200+startwin)
CGFcut=qqq.slice(endtime=qqq[0].stats.starttime+endwin-startwin)
CGFcut.detrend('linear')
CGFcut.detrend("demean")
qqq=RGF.slice(starttime=200+startwin)
RGFcut=qqq.slice(endtime=qqq[0].stats.starttime+endwin-startwin)
RGFcut.detrend('linear')
RGFcut.detrend("demean")

ori_itera=(endwin-startwin)/2
overlapping_itera=2*ori_itera-1 # 50% overlapped

midtime=[]
shift=[]
# for mm in range(0,int(overlapping_itera)):
for mm in range(0,1):
    window_begin=mm
    st_win_beg=window_begin
    st_win_end=st_win_beg+2
    window=correlate_python(CGFcut[0].data,RGFcut[0].data)
    tt=np.linspace(0,endwin-startwin ,18*40+1)
    delta=CGFcut[0].stats.delta
    fi = scipy.fftpack.fftfreq(tt.size,delta)
    X = scipy.fftpack.fft(CGFcut[0].data)
    Y = scipy.fftpack.fft(RGFcut[0].data)
    Sxx=abs(X)**2
    Syy=abs(Y)**2
    Sxy=X*Y.conjugate()
    phase=[]
    for i in range(len(Sxy)):
        phase.append(math.atan(Sxy[i].imag/Sxy[i].real/(2*np.pi)))
        Sxy[i]=abs(Sxy[i])*np.exp(complex(0, 1)*phase[i])
    Sxy_time = fftshift(scipy.fftpack.ifft(Sxy))
    Ci=abs(Sxy)/np.sqrt(Sxx*Syy)
    
    # W=Sxy*(Ci**2)/(1-Ci**2)
    
    
    # npt=int(1/delta)
    # fNy = 1./(2.*delta)
    # freqqq = np.linspace(0, fNy, npt // 2 + 1)
      
        
#     
#     # print(st_win_beg+2,st_win_end+2)

#     CGF_win=(CGF_win[0].data)
#     RGF_win=(RGF_win[0].data)
    
    
#     
#     
#     

#     
#     # 
#     fqqq=[];fppp=[];wwww=[]
#     for kk in range(len(fi)):
#         if fi[kk]<float(freqmax) and fi[kk]>=float(freqmin):
#             fqqq.append(fi[kk])
#             fppp.append(phase[kk])
#             wwww.append(W[kk])
#     regr = LinearRegression()
#     Fi=fi.reshape(len(fi),1)
#     Fi=np.array(fqqq).reshape(len(fqqq),1)
#     Phase=np.array(phase).reshape(len(phase),1)
#     Phase=np.array(fppp).reshape(len(fppp),1)
#     W=normalized(W)
#     w=W.reshape(len(W),1)
#     w=np.array(wwww)
#     regr.fit(Fi,Phase, sample_weight=w)
#     # # #### plot ####
#     plot_data_wave_ww = 0
#     plot_parameter_data=0
#     if plot_data_wave_ww:
#         plot_data(tt,RGF_win,CGF_win,0,2)
#     if plot_parameter_data:
#         plot_parameter(fi,Ci,W,Sxy,freqmin,freqmax,mm,fqqq,fppp,regr.coef_[0],regr.intercept_[0])

#     print(str(st_win_beg+2)+'-'+str(st_win_end+2)+' sec:',round((float(regr.coef_)/np.pi/2),4))
#     midtime.append((st_win_beg+2+st_win_end+2)/2)
#     shift.append(round((float(regr.coef_[0])/np.pi/2),8))
    

# plt.scatter(midtime,shift)
# midtime=np.array(midtime).reshape(-1,1)
# shift=np.array(shift).reshape(-1,1)
# rrr = LinearRegression(fit_intercept = False).fit(midtime,shift)
# pred= midtime * rrr.coef_[0] 
# plt.plot(midtime,pred,c='r')
# print(rrr.coef_[0])
def get_event_list(str1,str2,inc_hours):
    '''
    this function calculates the event list between time1 and time2 by increment of inc_hours
    in the formate of %Y_%m_%d_%H_%M_%S' (used in S0A & S0B)
    PARAMETERS:
    ----------------    
    str1: string of the starting time -> 2010_01_01_0_0
    str2: string of the ending time -> 2010_10_11_0_0
    inc_hours: integer of incremental hours
    RETURNS:
    ----------------
    event: a numpy character list 
    '''
    date1=str1.split('_')
    date2=str2.split('_')
    y1=int(date1[0]);m1=int(date1[1]);d1=int(date1[2])
    h1=int(date1[3]);mm1=int(date1[4]);mn1=int(date1[5])
    y2=int(date2[0]);m2=int(date2[1]);d2=int(date2[2])
    h2=int(date2[3]);mm2=int(date2[4]);mn2=int(date2[5])    
  
    d1=datetime.datetime(y1,m1,d1,h1,mm1,mn1)
    d2=datetime.datetime(y2,m2,d2,h2,mm2,mn2)
    dt=datetime.timedelta(hours=inc_hours)

    event = []
    while(d1<d2):
        event.append(d1.strftime('%Y_%m_%d_%H_%M_%S'))
        d1+=dt
    event.append(d2.strftime('%Y_%m_%d_%H_%M_%S'))
    
    return event