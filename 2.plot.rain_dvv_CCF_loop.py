#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 23:52:02 2020

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


LIM=0.2
uu='CGF5days_4s_0.2'
time=dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2020, 1, 1, 0, 0)
# pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
pair_list=['CHS5-CHS4']
# HZ_list = [[1,4],[3,6],[5,8]]
HZ_list = [[1,4]]
# window_list = [[2,6],[3,7],[4,8],[5,9],[6,10],[7,11],[8,12],[2,10]]
window_list = [[2,6]]
for pair in pair_list:
    for a in range (len(HZ_list)):
        freqmin = HZ_list[a][0]
        freqmax = HZ_list[a][1]
        for b in range(len(window_list)):
            xmin = window_list[b][0]
            xmax = window_list[b][1]
            HZ = str(freqmin)+'_'+str(freqmax) 
            window= str(xmin)+'_'+str(xmax)
            plt.rcParams['figure.figsize'] =30,15
            # fig, ax = plt.subplots(nrows=5,ncols=1,gridspec_kw={'height_ratios':[2,3,3,5,5]}) 
            fig, ax = plt.subplots(nrows=3,ncols=1,gridspec_kw={'height_ratios':[3,3,2]}) 
            #=================================地下水=============================================
            # waterpath1='D:/2020summer/池上/中城地下水.csv'
            # grounddate=[];groundwater=[];UTCground=[]
            # with open (waterpath1,newline='') as wfile:
            #     rows=list(csv.reader(wfile,delimiter=','))
            #     for row in rows[1:]:
            #         if float(row[1])!=0:
            #             grounddate.append(row[0])
            #             groundwater.append(131.4830-float(row[1]))
            #     for UUU in grounddate:
            #         year=UUU.rsplit('/',3)[0]
            #         month=UUU.rsplit('/',3)[1]
            #         day=UUU.rsplit('/',3)[2]
            #         UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
            #         UTCground.append(UTC)
            waterpath2='D:/2020summer/池上/池上地下水.csv'
            grounddate2=[];groundwater2=[];UTCground2=[]
            with open (waterpath2,newline='') as wfile:
                rows=list(csv.reader(wfile,delimiter=','))
                for row in rows[1:]:
                    if float(row[1])!=0:
                        grounddate2.append(row[0])
                        groundwater2.append(float(row[1])-286)
                for UUU in grounddate2:
                    year=UUU.rsplit('/',3)[0]
                    month=UUU.rsplit('/',3)[1]
                    day=UUU.rsplit('/',3)[2]
                    UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
                    UTCground2.append(UTC)
            ax2 = ax[2].twinx()
            ax2.plot(UTCground2,groundwater2,c='blue',lw=5,ls='-')
            # ax2.plot(UTCground,groundwater,c='blue',lw=5,ls='-')
            ax2.set_xlim(time)
            ax2.set_ylim(-35,0)
            ax2.tick_params(axis='y', labelcolor='blue')
            ax2.set_ylabel('Groundwater Depth (m)',c='blue',fontsize=20)
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
            # # ax[0].plot(UTCttt,ttt,c = 'g',lw = 5,ls = '-')
            # ax[0].plot(UTCttt,hpa,c = 'g',lw = 5,ls = '-')
            
            #=================================周雨量=============================================
            formatter = DateFormatter('20%y')
            newrain=[]
            newUTC=[]
            path = 'D:/2020summer/CHS/Chihshang_prep_finish/weekkk/'
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
                        
                        
            ax[2].bar(newUTC,newrain,width=10,color = 'gray')
            ax[2].set_xlim(time)
            # plt.xlabel('Year',fontsize=17)
            ax[2].set_ylabel('Precipitation (mm)\n',fontsize=17)
            ax[2].set_xticklabels(labels=[],fontsize=15)
            ax[2].set_xticklabels(labels=[],fontsize=15)
            ax[2].tick_params(axis='both',labelsize=15)
            # ax[0].set_yscale("log")
            # ax[0].set_title(pair+'  w='+window+'  hz='+HZ+' LIM='+str(LIM),fontsize=50,fontweight='bold')
            locator = YearLocator()
            ax[2].xaxis.set_major_locator(locator)
            ax[2].xaxis.set_major_formatter(formatter)
            ax[2].tick_params(which='major', length=7)
            minloc = AutoDateLocator()
            minloc.intervald[MONTHLY] = [6]
            ax[2].xaxis.set_minor_locator(minloc)
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
                
            ax[0].axhline(y=0,color='lightgrey')
            aaa=ax[0].scatter(CGF_day_list,shift_p,c=coeff_p,cmap='rainbow',lw=1,vmin=0.0, vmax=1)
            ax[0].set_ylabel('positive dv/v',fontsize=20)
            ax[0].set_xlim(time)
            ax[0].grid(axis='x')
            ax[0].set_xticklabels(labels=[],fontsize=15)
            ax[0].tick_params(which='major', length=12,labelsize=20)
            ax[0].set_ylim(LIM,-LIM)
            ax[0].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
            ax[0].tick_params(which='minor', length=10,labelsize=20)
            # ax2.xaxis.set_major_locator(ticker.MultipleLocator(3.00))
            #================================dvv_negative==============================================
            CGF_day_list=[]
            for i , UTC in enumerate(JJJ):
                yyyy=UTC.rsplit('/',1)[0]
                jjj=UTC.rsplit('/',1)[1]
                aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
                UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
                CGF_day_list.append(UUU)
                
            ax[1].axhline(y=0,color='lightgrey')
            aaa=ax[1].scatter(CGF_day_list,shift_n,c=coeff_n,cmap='rainbow',lw=1,vmin=0.0, vmax=1)
            ax[1].set_ylabel('negative dv/v',fontsize=20)
            ax[1].set_xlim(time)
            ax[1].grid(axis='x')
            ax[1].set_xticklabels(labels=[],fontsize=15)
            ax[1].tick_params(which='major', length=12,labelsize=20)
            ax[1].set_ylim(LIM,-LIM)
            ax[1].xaxis.set_minor_locator(mpl.dates.MonthLocator(interval=3))
            ax[1].tick_params(which='minor', length=10,labelsize=20)
            # ax2.xaxis.set_major_locator(ticker.MultipleLocator(3.00))
            cax = plt.axes([0.91, 0.35, 0.01, 0.51])
            cbr=fig.colorbar(aaa, cax=cax)
            cbr.set_label('Coefficient',fontsize=22)
            #====================================CCF_positive==========================================
            # CCF_DIR="D:/2020summer/CHS/D03_CCF"
            # bbb=10**-1.5
            # file1=sorted(glob.glob(CCF_DIR+'/'+pair+'/*CCF'))[0]
            # yyyy1=file1.rsplit('.',5)[1]
            # jul1=file1.rsplit('.',5)[2]
            # UTC1=UTCDateTime(year=int(yyyy1),julday=int(jul1), hour=00, minute=0)
            # file2=sorted(glob.glob(CCF_DIR+'/'+pair+'/*CCF'))[-2]
            # yyyy2=file2.rsplit('.',5)[1]
            # jul2=file2.rsplit('.',5)[2]
            # UTC2=UTCDateTime(year=int(yyyy2),julday=int(jul2), hour=00, minute=0)
            
            # date1 = dt.datetime(UTC1.year, UTC1.month, UTC1.day)
            # date2 = dt.datetime(UTC2.year, UTC2.month, UTC2.day)
            # delta= dt.timedelta(days=1)
            # dates= mpl.dates.drange(date1, date2, delta)
            
            # oldyyyy=0
            # for a,UTC in enumerate(dates):
            #     UUU=UTCDateTime(mpl.dates.num2date(UTC))
            #     yyyy=str(UUU.year)
            #     y2=1.5*a*bbb
            #     if int(yyyy)<=2016 and int(yyyy)>=2013:
            #         jjj=str(UUU.julday)
            #         if len(jjj)==1:
            #             jjj='00'+jjj
            #         elif len(jjj)==2:
            #             jjj='0'+jjj
            #         else: jjj=jjj
                    
            #         if sorted(glob.glob(CCF_DIR+'/'+pair+'/*'+yyyy+'.'+jjj+'*CCF'))==[]:
            #             continue
            #         msdpath=sorted(glob.glob(CCF_DIR+'/'+pair+'/*'+yyyy+'.'+jjj+'*CCF'))[0]
            #         print(msdpath)
            #         st=read(msdpath)  
            #         st.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
            #         data=st[0].data
            #         lags=np.arange((200+xmin)*(1/st[0].stats.delta),(200+xmax)*(1/st[0].stats.delta))
            #         data_new = data[int((200+xmin)*(1/st[0].stats.delta)):int((200+xmax)*(1/st[0].stats.delta))]
            #         ax[3].fill_betweenx(lags/(1/st[0].stats.delta) ,data_new+y2,y2,where=data_new+y2<y2,lw=1.5,color='lightskyblue', alpha=0.7)
            #         ax[3].fill_betweenx(lags/(1/st[0].stats.delta) ,data_new+y2, y2,where=data_new+y2>y2,lw=1.5,color='violet', alpha=0.7)
            #         ax[3].plot(data_new+y2,lags/(1/st[0].stats.delta),'grey',lw=0.5)
                    
            #         # if int(jjj)%50 ==1:
            #         #     ax[3].text(y2,xmax+0.3,jjj,fontsize= 12)
            #         # elif int(yyyy) != int(oldyyyy):
            #         #     ax[3].text(y2-0.01,xmax+0.9,yyyy,fontsize=18)
            #         #     oldyyyy=yyyy
                
            # ax[3].set_ylabel('Lags (s)',fontsize=20)
            # ax[3].set_xlabel('\n\nJulian Day',fontsize=20)
            # ax[3].set_xticks([])
            # ax[3].set_yticks(range(200+xmin,201+xmax,1)) 
            # ax[3].set_yticklabels((str(xmin),str(int((xmax+xmin-1)/2)),str(int((xmax+xmin+1)/2)),str(xmax)),fontsize=20)
            # ax[3].tick_params(axis='y',labelsize=15)
            # ax[3].set_ylim(200+xmin,200+xmax)
            # ax[3].set_title(pair+'bp'+str(freqmin)+'-'+str(freqmax)+'Hz',fontsize=20)
            # #====================================CCF_negative==========================================
            # for a,UTC in enumerate(dates):
            #     UUU=UTCDateTime(mpl.dates.num2date(UTC))
            #     yyyy=str(UUU.year)
            #     y2=1.5*a*bbb
            #     if int(yyyy)<=2016 and int(yyyy)>=2013:
            #         jjj=str(UUU.julday)
            #         if len(jjj)==1:
            #             jjj='00'+jjj
            #         elif len(jjj)==2:
            #             jjj='0'+jjj
            #         else: jjj=jjj
                    
            #         if sorted(glob.glob(CCF_DIR+'/'+pair+'/*'+yyyy+'.'+jjj+'*CCF'))==[]:
            #             continue
            #         msdpath=sorted(glob.glob(CCF_DIR+'/'+pair+'/*'+yyyy+'.'+jjj+'*CCF'))[0]
            #         print(msdpath)
            #         st=read(msdpath)  
            #         st.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=4,zerophase=True)
            #         data=st[0].data
            #         lags=np.arange((200-xmax)*(1/st[0].stats.delta),(200-xmin)*(1/st[0].stats.delta))
            #         data_new = data[int((200-xmax)*(1/st[0].stats.delta)):int((200-xmin)*(1/st[0].stats.delta))]
            #         ax[4].fill_betweenx(lags/(1/st[0].stats.delta) ,data_new+y2,y2,where=data_new+y2<y2,lw=1.5,color='lightskyblue', alpha=0.7)
            #         ax[4].fill_betweenx(lags/(1/st[0].stats.delta) ,data_new+y2, y2,where=data_new+y2>y2,lw=1.5,color='violet', alpha=0.7)
            #         ax[4].plot(data_new+y2,lags/(1/st[0].stats.delta),'grey',lw=0.5)
                    
            #         # if int(jjj)%50 ==1:
            #         #     ax[3].text(y2,xmax+0.3,jjj,fontsize= 12)
            #         # elif int(yyyy) != int(oldyyyy):
            #         #     ax[3].text(y2-0.01,xmax+0.9,yyyy,fontsize=18)
            #         #     oldyyyy=yyyy
                
            # ax[4].set_ylabel('Lags (s)',fontsize=20)
            # ax[4].set_xlabel('\n\nJulian Day',fontsize=20)
            # ax[4].set_xticks([])
            # ax[4].set_yticks(range(200-xmax,201-xmin,1)) 
            # ax[4].set_yticklabels((str(-xmax),str(int((-xmax-xmin+1)/2)),str(int((-xmax-xmin-1)/2)),str(-xmin)),fontsize=20)
            # ax[4].tick_params(axis='y',labelsize=15)
            # ax[4].set_ylim(200-xmax,200-xmin)
            # ax[4].tick_params(axis='y',labelsize=15)
            # ax[4].set_title(pair+'bp'+str(freqmin)+'-'+str(freqmax)+'Hz',fontsize=20)
            
            #====================================save figure==========================================            
            fig.savefig('D:/TGA/CHS/2013-2019/'+pair+'_'+window+'_'+HZ+'_'+str(LIM)+'_water.jpg')
            print('D:/TGA/CHS/2013-2019'+'/'+pair+'_'+window+'_'+HZ+'_'+str(LIM)+'_water.jpg Save-------')
            plt.cla()
            plt.show()
            # plt.close()
            
