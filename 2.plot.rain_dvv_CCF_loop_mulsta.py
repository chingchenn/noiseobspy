# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 21:58:40 2020

@author: grace
"""


import csv
import glob
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from matplotlib.dates import (YearLocator, MONTHLY,DateFormatter,AutoDateLocator)


LIM=0.1
uu='CGF5days_4s_0.2'
time=dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2020, 1, 1, 0, 0)
pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
# pair_list=['CHS5-CHS4']
HZ_list = [[1,4],[3,6],[5,8]]
# HZ_list = [[3,6]]
window_list = [[2,6],[3,7],[4,8],[5,9],[6,10],[7,11],[8,12],[2,10]]
# window_list = [[3,7]]
for pair in pair_list:
    for a in range (len(HZ_list)):
        freqmin = HZ_list[a][0]
        freqmax = HZ_list[a][1]
        for b in range(len(window_list)):
            xmin = window_list[b][0]
            xmax = window_list[b][1]
            HZ = str(freqmin)+'_'+str(freqmax) 
            window= str(xmin)+'_'+str(xmax)
            plt.rcParams['figure.figsize'] =30,16
            # fig, ax = plt.subplots(nrows=5,ncols=1,gridspec_kw={'height_ratios':[2,3,3,5,5]}) 
            fig, ax = plt.subplots(nrows=4,ncols=1,gridspec_kw={'height_ratios':[2,2,3,3]}) 
            #=================================地下水之其它站=============================================
            waterpath1='D:/2020summer/池上/中城地下水.csv'
            grounddate=[];groundwater=[];UTCground=[]
            with open (waterpath1,newline='') as wfile:
                rows=list(csv.reader(wfile,delimiter=','))
                for row in rows[1:]:
                    if float(row[1])!=0:
                        grounddate.append(row[0])
                        groundwater.append(131.483-float(row[1]))
                for UUU in grounddate:
                    year=UUU.rsplit('/',3)[0]
                    month=UUU.rsplit('/',3)[1]
                    day=UUU.rsplit('/',3)[2]
                    UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
                    UTCground.append(UTC)
            waterpath2='D:/2020summer/池上/學田地下水.csv'
            grounddate2=[];groundwater2=[];UTCground2=[]
            with open (waterpath2,newline='') as wfile:
                rows=list(csv.reader(wfile,delimiter=','))
                for row in rows[1:]:
                    if float(row[1])!=0:
                        grounddate2.append(row[0])
                        groundwater2.append(248.7340-float(row[1]))
                for UUU in grounddate2:
                    year=UUU.rsplit('/',3)[0]
                    month=UUU.rsplit('/',3)[1]
                    day=UUU.rsplit('/',3)[2]
                    UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
                    UTCground2.append(UTC)
            ax[0].plot(UTCground,groundwater,c='blue',lw=5,ls='-')
            ax[0].plot(UTCground2,groundwater2,c='green',lw=5,ls='-')
            ax[0].set_xlim(time)
            ax[0].set_ylim(1,7)
            ax[0].tick_params(axis='y', labelcolor='blue')
            ax[0].set_ylabel('Groundwater\n elevation (m)\n',c='blue',fontsize=20)
            
            #================================地下水=============================================
            waterpath1='D:/2020summer/池上/池上地下水.csv'
            grounddate=[];groundwater=[];UTCground=[]
            with open (waterpath1,newline='') as wfile:
                rows=list(csv.reader(wfile,delimiter=','))
                for row in rows[1:]:
                    if float(row[1])!=0:
                        grounddate.append(row[0])
                        groundwater.append(286-float(row[1]))
                for UUU in grounddate:
                    year=UUU.rsplit('/',3)[0]
                    month=UUU.rsplit('/',3)[1]
                    day=UUU.rsplit('/',3)[2]
                    UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
                    UTCground.append(UTC)
            
            ax2 = ax[1].twinx()
            ax2.plot(UTCground,groundwater,c='blue',lw=5,ls='-')
            ax2.set_xlim(time)
            # ax2.set_ylim(35,10)
            ax2.tick_params(axis='y', labelcolor='blue')
            # ax2.set_ylabel('Groundwater elevation (m)',c='blue',fontsize=20)
            ax[0].set_title(pair+'  w='+window+'  hz='+HZ+' LIM='+str(LIM),fontsize=50,fontweight='bold')
            # #================================氣溫氣壓==============================================
            # tempeturepath = 'D:/2020summer/池上/TEMPETURE/monthdata/tt.csv'
            # tttdate = [];ttt = [];UTCttt = [];hpa = []
            # with open (tempeturepath,newline='') as wfile:
            #     rows=list(csv.reader(wfile,delimiter=','))
            #     for row in rows[1:]:
            #         if row[2]=='/' or row[2]=='...':
            #             break
            #         tttdate.append(row[1])
            #         ttt.append(float(row[2]))
            #         hpa.append(float(row[3]))
            #     for UUU in tttdate:
            #         year=UUU.rsplit('-',3)[0]
            #         month=UUU.rsplit('-',3)[1]
            #         day=UUU.rsplit('-',3)[2]
            #         UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
            #         UTCttt.append(UTC)
            # # ax[1].plot(UTCttt,ttt,c = 'g',lw = 5,ls = '-')
            # ax[1].plot(UTCttt,hpa,c = 'k',lw = 5,ls = '-')
            
            #=================================周雨量=============================================
            formatter = DateFormatter('20%y')
            newrain=[]
            newUTC=[]
            path = 'D:/2020summer/CHS/Chihshang_prep_finish/'
            for i,csvfile in enumerate(sorted(glob.glob(path+'*weekkk.csv'))):
                sta = (csvfile.rsplit('/',4)[-1].rsplit('\\',2)[1]).rsplit('_',3)[0]
                df = pd.read_csv(csvfile, encoding= 'unicode_escape')
                date = np.array(df.Time).tolist()
                rain= np.array(df.Prep).tolist()
                
                for r in rain:
                    if r == str('T')  :
                        r = 0
                    elif r==str("...") :
                        r = 0
                    elif r ==str('X'):
                        r = 0
                    newrain.append(float(r))
                for U in date:
                    yyyy1=int(str(U)[0:4])
                    mm1=int(str(U)[4:6])
                    dd1=int(str(U)[6:8])
            
                    date3=UTCDateTime(year=yyyy1,month=mm1,day=dd1)
                    UTC1=dt.datetime(year=date3.year, month=date3.month, day=date3.day,fold=1)
            
                    newUTC.append(UTC1)
                        
                        
            ax[1].bar(newUTC,newrain,width=10,color = 'gray')
            ax[1].set_xlim(time)
            # plt.xlabel('Year',fontsize=17)
            ax[1].set_ylabel('Precipitation (mm)\n',fontsize=17)
            ax[1].set_xticklabels(labels=[],fontsize=15)
            ax[1].set_xticklabels(labels=[],fontsize=15)
            ax[1].tick_params(axis='both',labelsize=15)
            ax[1].set_yscale("log")
            locator = YearLocator()
            ax[1].xaxis.set_major_locator(locator)
            ax[1].xaxis.set_major_formatter(formatter)
            ax[1].tick_params(which='major', length=7)
            minloc = AutoDateLocator()
            minloc.intervald[MONTHLY] = [6]
            ax[1].xaxis.set_minor_locator(minloc)
            #================================dvv_positive==============================================
            csvpath = 'D:/2020summer/CHS/stretching/count/'+uu+'/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'.csv'
            df = pd.read_csv(glob.glob(csvpath)[0])
            shift_n=df.dvv_n
            shift_p=df.dvv_p
            coeff_n=df.coeff_n
            coeff_p=df.coeff_p
            JJJ=list(df.juliday)
            
            def strjjj(jjj):
                jjj=str(jjj)
                if len(jjj)==1:
                    return '00'+jjj
                elif len(jjj)==2:
                    return '0'+jjj
                else: return jjj
            CGF_day_list=[]
            for i , UTC in enumerate(JJJ):
                yyyy=UTC.rsplit('/',1)[0]
                jjj=UTC.rsplit('/',1)[1]
                aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
                UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
                CGF_day_list.append(UUU)
                
            ax[2].axhline(y=0,color='lightgrey')
            aaa=ax[2].scatter(CGF_day_list,shift_p,c=coeff_p,cmap='rainbow',lw=1,vmin=0.0, vmax=1)
            ax[2].set_ylabel('positive dv/v',fontsize=20)
            ax[2].set_xlim(time)
            ax[2].grid(axis='x')
            ax[2].set_xticklabels(labels=[],fontsize=15)
            ax[2].tick_params(which='major', length=12,labelsize=20)
            ax[2].set_ylim(-LIM,LIM)
            ax[2].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
            ax[2].tick_params(which='minor', length=10,labelsize=20)
            # ax2.xaxis.set_major_locator(ticker.MultipleLocator(3.00))
            #================================dvv_negative==============================================
            CGF_day_list=[]
            for i , UTC in enumerate(JJJ):
                yyyy=UTC.rsplit('/',1)[0]
                jjj=UTC.rsplit('/',1)[1]
                aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
                UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
                CGF_day_list.append(UUU)
                
            ax[3].axhline(y=0,color='lightgrey')
            aaa=ax[3].scatter(CGF_day_list,shift_n,c=coeff_n,cmap='rainbow',lw=1,vmin=0.0, vmax=1)
            ax[3].set_ylabel('negative dv/v',fontsize=20)
            ax[3].set_xlim(time)
            ax[3].grid(axis='x')
            ax[3].set_xticklabels(labels=[],fontsize=15)
            ax[3].tick_params(which='major', length=12,labelsize=20)
            ax[3].set_ylim(-LIM,LIM)
            ax[3].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
            ax[3].tick_params(which='minor', length=10,labelsize=20)
            # ax2.xaxis.set_major_locator(ticker.MultipleLocator(3.00))
            cax = plt.axes([0.91, 0.345, 0.01, 0.2])
            cbr=fig.colorbar(aaa, cax=cax)
            cbr.set_label('Coefficient',fontsize=22)
            
            #====================================save figure========================================== 
            fig.savefig('D:/TGA/CHS/2013-2019/'+pair+'_'+window+'_'+HZ+'_'+str(LIM)+'_water2sta.jpg')
            print('D:/TGA/CHS/2013-2019'+'/'+pair+'_'+window+'_'+HZ+'_'+str(LIM)+'_water2sta.jpg Save-------')
            plt.cla()
            plt.show()