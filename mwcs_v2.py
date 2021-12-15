# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:22:35 2020

@author: grace
"""

#每兩秒算一次ccf
import math
import scipy
import numpy as np
import pandas as pd
import numpy.fft as fft
from plot_mwcs import *
from scipy import signal
import sys, obspy, os,glob
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from scipy.optimize import leastsq
from obspy.core.stream import Stream
from obspy import read, read_inventory,Trace
from numpy.fft import ifft, fftshift,fftfreq
from obspy.geodetics import locations2degrees
from sklearn.linear_model import LinearRegression

plt.rcParams['figure.figsize']=15,11.25
SAC_DIR= 'D:/2020summer/CHS/stretching/'
CGF='D:/2020summer/CHS/stretching/02_CHS5-CHS4_CGF5days/CHS5-CHS4.2016.222.HHZ.CGF'
RGF='D:/2020summer/CHS/D04_stk/CHS5-CHS4.HHZ.stk'
freqmin=1
freqmax=4
endwin=20
startwin=2
CGF = read(CGF)
RGF = read(RGF)
lags=np.arange(-8000,8000)
delta=CGF[0].stats.delta
npt=int(1/delta)
fNy = 1./(2.*delta)
freqqq = np.linspace(0, fNy, npt // 2 + 1)
plot_data_wave = 0
if plot_data_wave:
    plot_data(lags/40,RGF[0].data,CGF[0].data,startwin,endwin)
CGF.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
RGF.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)


# 選取時間段(正時間)
qqq=CGF.slice(starttime=200+startwin)
CGFcut=CGF.slice(endtime=qqq[0].stats.starttime+endwin-startwin)
CGFcut.detrend('linear')
CGFcut.detrend("demean")
RGFcut=RGF.slice(endtime=qqq[0].stats.starttime+endwin-startwin)
RGFcut.detrend('linear')
RGFcut.detrend("demean")

win_len=6
ori_itera=(endwin-startwin)/6
overlapping_itera=2*ori_itera-1 # 50% overlapped
win_frac=overlapping_itera
midtime=[]
shift=[]
for mm in range(0,int(overlapping_itera)):
# for mm in range(0,2):
    nstat = len(CGFcut)
    fs = CGFcut[0].stats.sampling_rate
    nsamp = int(win_len * fs)
    nstep = int(nsamp * win_frac)
    nfft = nextpow2(nsamp)
    deltaf = fs / float(nfft)
    nlow = int(freqmin / float(deltaf) + 0.5)
    nhigh = int(freqmax / float(deltaf) + 0.5)
    nlow = max(1, nlow)  # avoid using the offset
    nhigh = min(nfft // 2 - 1, nhigh)  # avoid using nyquist
    nf = nhigh - nlow + 1  # include upper and lower frequency
    # to speed up the routine a bit we estimate all steering vectors in advance
    tap = cosine_taper(nsamp, p=0.22)
    
    
    window_begin=mm*3
    st_win_beg=window_begin
    st_win_end=st_win_beg+6
    CGF_win=CGFcut.slice(starttime=qqq[0].stats.starttime+st_win_beg,endtime=qqq[0].stats.starttime+st_win_end)
    RGF_win=RGFcut.slice(starttime=qqq[0].stats.starttime+st_win_beg,endtime=qqq[0].stats.starttime+st_win_end)
    CGF_win.detrend('linear')
    RGF_win.detrend('linear')
    CGF_win.detrend("demean")
    RGF_win.detrend("demean")
    tt=np.linspace(0, 6, 241)
    print(st_win_beg+2,st_win_end+2)

    # CGF_win=(CGF_win[0].data)
    # RGF_win=(RGF_win[0].data)
    
    
    # X = scipy.fftpack.fft(CGF_win)
    # Y = scipy.fftpack.fft(RGF_win)
    # Sxx=np.sqrt((X.real)**2+(X.imag)**2)
    # Syy=np.sqrt((Y.real)**2+(Y.imag)**2)
    # Sxy=X*Y.conjugate()
    # Sxy_time = fftshift(scipy.fftpack.ifft(Sxy))
    # corr = correlate_python(CGF_win,RGF_win)
    # # Ci=abs(Sxy)/np.sqrt((Sxx**2)*(Syy**2))
    # # W=abs(Sxy)*(Ci**2)/(1-Ci**2)
    # phase=[]
    # for i in range(len(Sxy)):
    #     phase.append(math.atan(Sxy[i].imag/Sxy[i].real/(2*np.pi)))

    # fi = scipy.fftpack.fftfreq(tt.size,delta)
    # # fi = scipy.fftpack.fftfreq(CGF[0].stats.npts, delta)
    # # fqqq=[];fppp=[];wwww=[]
    # # for kk in range(len(fi)):
    # #     if fi[kk]<float(freqmax) and fi[kk]>=float(freqmin):
    # #         fqqq.append(fi[kk])
    # #         fppp.append(phase[kk])
    # #         wwww.append(W[kk])
    # # regr = LinearRegression()
    # # Fi=fi.reshape(len(fi),1)
    # # Fi=np.array(fqqq).reshape(len(fqqq),1)
    # # Phase=np.array(phase).reshape(len(phase),1)
    # # Phase=np.array(fppp).reshape(len(fppp),1)
    # # W=normalized(W)
    # # w=W.reshape(len(W),1)
    # # w=np.array(wwww)
    # # regr.fit(Fi,Phase, sample_weight=w)
    # # # #### plot ####
    # plot_data_wave_ww = 0
    # plot_parameter_data=0
    # if plot_data_wave_ww:
    #     plot_data(tt,RGF_win,CGF_win,0,6)
    # # if plot_parameter_data:
    # #     plot_parameter(fi,Ci,W,Sxy,freqmin,freqmax,mm,fqqq,fppp,regr.coef_[0],regr.intercept_[0])

    # # print(str(st_win_beg+2)+'-'+str(st_win_end+2)+' sec:',round((float(regr.coef_)/np.pi/2),4))
    # # midtime.append((st_win_beg+2+st_win_end+2)/2)
    # # shift.append(round((float(regr.coef_[0])/np.pi/2),8))
    
    # ###TEST convelution and correlation###
    # corr = scipy.signal.correlate(RGF_win,CGF_win,mode='full',method='direct')
    # concon=X*Y.conjugate()
        
    # CONCON=fftshift(scipy.fftpack.ifft(concon))
    # Syx=X.conjugate()*Y
    # Syx_new = fftshift(scipy.fftpack.ifft(Syx))
    # vvvv = scipy.signal.convolve(CGF_win,RGF_win,mode='full',method='direct')

# plt.scatter(midtime,shift,c='k')
# midtime=np.array(midtime).reshape(-1,1)
# shift=np.array(shift).reshape(-1,1)
# rrr = LinearRegression(fit_intercept = False).fit(midtime,shift)
# pred= midtime * rrr.coef_[0] 
# plt.plot(midtime,pred,c='r')
# print(rrr.coef_[0])