# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:24:30 2020

@author: grace
"""




import os
import glob
import copy
import obspy
import scipy
import numpy as np
import pandas as pd
from numba import jit
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from obspy.signal.util import _npts2nfft
from obspy.signal.invsim import cosine_taper
from scipy.fftpack import fft,ifft,next_fast_len
from obspy.signal.filter import bandpass,lowpass
from obspy.signal.regression import linear_regression
from obspy.core.util.base import _get_function_from_entry_point


def dot_python(a, b, start, stop, delay):
    sum = 0
    for n in range(start, stop):
        sum += a[n + delay] * b[n]
    return sum
def correlate_python(a, b):
    size = len(a)
    c = [0] * size  # allocate output array/list
    for index in range(size):
        delay = index - size // 2
        if delay < 0:
            c[index] = dot_python(a, b, -delay, size, delay)
        else:
            c[index] = dot_python(a, b, 0, size-delay, delay)
    return c

def normalized(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

def plot_data(time,RGF,CGF,startwin,endwin):
     plt.plot(time,CGF,'r',label='CGF')
     plt.plot(time,RGF,'k',label='RGF')
     plt.xlim(startwin,endwin)
     plt.legend(loc=4,fontsize=35)
     plt.xticks(fontsize=20)
     plt.show()

def plot_parameter(fi,Ci,W,Sxy,freqmin,freqmax,mm,fqqq,fppp,a,b):
    fig,axs=plt.subplots(2,2)
    fig.suptitle(str(mm+2)+'-'+str(mm+4)+'  sec',fontsize=40)
    # axs[1,0].plot(fi, regr.predict(Fi), color='red', linewidth=3, label='Weighted model')
    # axs[1,0].scatter(fi,Phase,s=np.sqrt(np.sqrt(W))*10**4,c='b')
    ppp=a*fqqq+b
    # axs[1,0].plot(fqqq, regr.predict(Fi), color='red', linewidth=3, label='Weighted model')
    axs[1,0].plot(fqqq, ppp, color='red', linewidth=3, label='Weighted model')
    axs[1,0].scatter(fqqq,fppp,s=np.sqrt(W)*10**2*3/max(W),c='b')
    # axs[1,0].set_xlim(freqmin,freqmax)
    # axs[1,0].set_ylim(-0.5,0.5)
    
    
    axs[0,0].scatter(fi,Ci,s=20,c='k')
    axs[0,0].set_xlim(freqmin,freqmax)
    axs[0,0].set_ylim(min(Ci),max(Ci))
    axs[0,0].set_title('cohence',fontsize=20)
    axs[0,0].set_yticks([])
    axs[0,1].scatter(fi,W,s=20,c='k')
    axs[0,1].set_xlim(freqmin,freqmax)
    axs[0,1].set_ylim(min(W),max(W))
    axs[0,1].set_title('wight',fontsize=20)
    axs[0,1].set_yticks([])
    axs[1,1].scatter(fi,Sxy,s=20,c='k')
    axs[1,1].set_xlim(freqmin,freqmax)
    axs[1,1].set_ylim(min(Sxy),max(Sxy))
    axs[1,1].set_title('Sxy',fontsize=20)
    axs[1,1].set_yticks([])
    axs[1,1].set_xlabel('frequency (Hz)')
    plt.show()
    
    
def taper(data):
    '''
    this function applies a cosine taper using obspy functions
    PARAMETERS:
    ---------------------
    data: input data matrix
    RETURNS:
    ---------------------
    data: data matrix with taper applied
    '''
    #ndata = np.zeros(shape=data.shape,dtype=data.dtype)
    if data.ndim == 1:
        npts = data.shape[0]
        # window length 
        if npts*0.05>20:wlen = 20
        else:wlen = npts*0.05
        # taper values
        func = _get_function_from_entry_point('taper', 'cosine')
        if 2*wlen == npts:
            taper_sides = func(2*wlen)
        else:
            taper_sides = func(2*wlen+1)
        # taper window
        win  = np.hstack((taper_sides[:wlen], np.ones(npts-2*wlen),taper_sides[len(taper_sides) - wlen:]))
        data *= win
    elif data.ndim == 2:
        npts = data.shape[1]
        # window length 
        if npts*0.05>20:wlen = 20
        else:wlen = npts*0.05
        # taper values
        func = _get_function_from_entry_point('taper', 'hann')
        if 2*wlen == npts:
            taper_sides = func(2*wlen)
        else:
            taper_sides = func(2*wlen + 1)
        # taper window
        win  = np.hstack((taper_sides[:wlen], np.ones(npts-2*wlen),taper_sides[len(taper_sides) - wlen:]))
        for ii in range(data.shape[0]):
            data[ii] *= win
    return data
# taaa=taper(CGF_win[0].data)


def nextpow2(n):
    '''
    求最接近数据长度的2的整数次方
    An integer equal to 2 that is closest to the length of the data
    
    Eg: 
    nextpow2(2) = 1
    nextpow2(2**10+1) = 11
    nextpow2(2**20+1) = 21
    '''
    return np.ceil(np.log2(np.abs(n))).astype('long')
