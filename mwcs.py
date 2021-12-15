# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 00:22:58 2020

@author: grace
"""


# 拿整段(+-200sec)CFG跟RGF做計算
import math
import scipy
import numpy.fft as fft
from numpy.fft import fft, ifft, fftshift,fftfreq
import numpy as np
import matplotlib.pyplot as plt
import numpy.fft as fft
import sys, obspy, os,glob
from obspy import read, read_inventory,Trace
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
from obspy import UTCDateTime


plt.rcParams['figure.figsize']=15,8
SAC_DIR= 'D:/2020summer/CHS/stretching/'
CGF='D:/2020summer/CHS/D03_CCF/CHS5-CHS4/CHS5-CHS4.2016.220.HHZ.CCF'
RGF='D:/2020summer/CHS/D04_stk/CHS5-CHS4.HHZ.stk'
CGF = read(CGF)
RGF = read(RGF)
CGF.filter('bandpass',freqmin=1,freqmax=8,corners=4,zerophase=True)
RGF.filter('bandpass',freqmin=1,freqmax=8,corners=4,zerophase=True)
lags=np.arange(-8000+1,8001)
delta=CGF[0].stats.delta
npt=int(1/delta)
X = fft.fft(CGF[0].data)
Y = fft.fft(RGF[0].data)
Ycon=Y.conjugate()
Sxx=np.abs(X)**2
Syy=np.abs(Y)**2
Sxy=X*Ycon
Sxy_new = fftshift(scipy.fftpack.ifft(Sxy))
corr = scipy.signal.correlate(RGF[0].data,CGF[0].data,mode='same',method='direct')
corrv = scipy.signal.correlate(CGF[0].data,RGF[0].data,mode='same',method='fft')
Ci=abs(Sxy)/np.sqrt(Sxx*Syy)
W=abs(Sxy)*(Ci**2)/(1-Ci**2)
phase=[]

for i in range(len(Sxy)):
    phase.append(math.atan(Sxy[i].imag/Sxy[i].real/(2*np.pi)))

fig,axs=plt.subplots(2,2)
fi = fft.fftfreq(CGF[0].stats.npts, delta)
axs[1,0].scatter(fi,phase,s=3,c='b')
axs[1,0].set_xlim(1,8)
axs[0,0].scatter(fi,Ci,s=3,c='k')
axs[0,0].set_xlim(1,8)
axs[0,1].scatter(fi,W,s=3,c='k')
axs[0,1].set_xlim(1,8)
axs[0,1].set_ylim(-0.001,0.003)
axs[1,1].scatter(fi,Sxy,s=3,c='k')
axs[1,1].set_xlim(1,8)
axs[0,0].set_yticks([])
axs[0,1].set_yticks([])
axs[1,1].set_yticks([])
axs[1,0].set_yticks([])


endwin=10
startwin=2
ori_itera=(endwin-startwin)/2
overlapping_itera=2*ori_itera-1 # 50% overlapped
CGFcut=CGF[0].data[int(startwin*(1/delta)):int(endwin*npt)]
RGFcut=RGF[0].data[int(startwin*(1/delta)):int(endwin*npt)]
# CGFcut=CGF.slice(starttime=st_win_beg,endtime=st_win_end,nearest_sample=True)
##########################################################################################
for mm in range(0,int(overlapping_itera)):
    window_begin=mm*npt
    st_win_beg=window_begin
    st_win_end=st_win_beg+npt*2
    CGFwin=CGFcut[st_win_beg:st_win_end]
    RGFwin=RGFcut[st_win_beg:st_win_end]
    tt=np.linspace(0, 2, 80)
    print(st_win_beg/40+2,st_win_end/40+2)
# st1_win=st1.slice(starttime=st_win_beg,endtime=st_win_end,nearest_sample=True)
# st2_win=st2.slice(starttime=st_win_beg,endtime=st_win_end,nearest_sample=True)
# st1_win=st1_win[0]
# st2_win=st2_win[0]