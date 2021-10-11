# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:12:38 2020

@author: grace
"""


import glob
import pandas as pd
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.core import UTCDateTime


pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
# pair_list = ['IT01-IT03','IT01-IT04','IT01-IT05','IT01-IT07','IT01-IT09','IT02-IT01','IT02-IT03','IT02-IT04','IT02-IT05','IT02-IT06','IT02-IT07','IT02-IT08','IT02-IT09','IT02-IT10',
#                'IT03-IT04','IT03-IT05','IT03-IT07','IT03-IT09','IT04-IT05','IT04-IT07','IT06-IT01','IT06-IT01','IT06-IT03','IT06-IT05','IT06-IT07','IT06-IT08','IT06-IT09','IT06-IT10',
#                'IT07-IT05','IT08-IT01','IT08-IT03','IT08-IT04','IT08-IT05','IT08-IT07','IT09-IT05','IT09-IT04','IT10-IT01','IT10-IT03','IT10-IT04','IT10-IT05','IT10-IT07','IT10-IT09']
# window_list = ['2_6','3_7','4_8','5_9','6_10','7_11','8_12','2_10']
# HZ_list = ['1_4','3_6','5_8']
pair_list = ['CHS5-CHS2']
window_list = ['3_7']
HZ_list = ['3_6']
LIM = 0.12
def strjjj(jjj):
    jjj=str(jjj)
    if len(jjj)==1:
        return '00'+jjj
    elif len(jjj)==2:
        return '0'+jjj
    else: return jjj
for pair in pair_list:
    for HZ in HZ_list:
        for window in window_list:
            fig, ax = plt.subplots(nrows=2,ncols=1,gridspec_kw={'height_ratios':[1,1]})
            plt.rcParams['figure.figsize'] =38,12
            csvpath='D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'_nolevel.csv'
            # csvpath='D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/ttt.csv'
            df = pd.read_csv(glob.glob(csvpath)[0])
            shift_n=df.dvv_n
            shift_p=df.dvv_p
            coeff_n=df.coeff_n
            coeff_p=df.coeff_p
            JJJ=list(df.juliday)
            time=dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2020, 12, 31, 0, 0)    
            CGF_day_list=[]
            for i , UTC in enumerate(JJJ):
                yyyy=UTC.rsplit('/',1)[0]
                jjj=UTC.rsplit('/',1)[1]
                aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
                UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
                CGF_day_list.append(UUU)
            ax[0].axhline(y=0,color='lightgrey')
            aaa=ax[0].scatter(CGF_day_list,shift_p,c=coeff_n,cmap='rainbow',lw=1,vmin=0.0, vmax=1.0)
            ax[0].set_ylabel('positive dv/v',fontsize=20)
            ax[0].set_xlim(time)
            ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
            ax[0].grid(axis='x')
            ax[0].set_xticklabels(labels=[],fontsize=15)
            ax[0].tick_params(which='major', length=12,labelsize=20)
            # ax[0].set_title(pair+'  w='+window+'  hz='+HZ,fontsize=22,fontweight='bold')
            ax[0].set_ylim(LIM,-LIM)
            # ax[0].text(dt.datetime(2013, 1, 30, 0, 0),0.14,'Negative',fontsize=30,bbox=dict(facecolor='pink', alpha=0.7))
            ax[0].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
            ax[0].tick_params(which='minor', length=10,labelsize=20)
            ax[1].axhline(y=0,color='lightgrey')
            ax[1].scatter(CGF_day_list,shift_n,c=coeff_p,cmap='rainbow',lw=1,vmin=0.0, vmax=1.0)      
            ax[1].set_ylabel('negative dv/v',fontsize=20)
            # ax[1].set_xlabel('UTC',fontsize=20)
            ax[1].set_xlim(time)
            # ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
            ax[1].grid(axis='x')
            ax[1].tick_params(which='major', length=12,labelsize=20)
            ax[1].set_ylim(LIM,-LIM)
            # ax[1].text(dt.datetime(2013, 1, 30, 0, 0),0.14,'Positive',fontsize=30,bbox=dict(facecolor='pink', alpha=0.7))
            ax[1].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
            ax[1].tick_params(which='minor', length=10,labelsize=20)
            plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
            cax = plt.axes([0.8, 0.1, 0.01, 0.81])
            cbr=fig.colorbar(aaa, cax=cax)
            cbr.set_label('Coefficient',fontsize=22)
                
            # fig.savefig( 'D:/TGA/CHS/2013-2019'+'/'+pair+'_w='+window+'_Hz='+HZ+'.jpg')
            print('D:/TGA/CHS/2013-2019'+'/'+pair+'_w='+window+'_Hz='+HZ+'.jpg DONE')
            plt.cla()
            plt.show()