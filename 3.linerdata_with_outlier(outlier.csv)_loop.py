# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 17:32:31 2020

@author: grace
"""

#算出線性回歸的理論值，存到_outlier.csv裡

import scipy as sp
import numpy as np
from pylab import *
import pandas as pd
import datetime as dt
from scipy import stats
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

pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
window_list = ['2_6','3_7','4_8','5_9','6_10','7_11','8_12']
HZ_list = ['1_4','3_6','5_8']
HZ_list = ['3_6','1_4']
window_list = ['3_7']
pair_list = ['CHS5-CHS4']
stkdays=5
for pair in pair_list:
    for window in window_list:
        for HZ in HZ_list:
            filename= 'D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'.csv'
            df=pd.read_csv(glob.glob(filename)[0])
            dn=df.dvv_n.tolist()
            dp=df.dvv_p.tolist()
            cncn=df.coeff_n.tolist()
            cpcp=df.coeff_p.tolist()
            lll=df.waterlevel.tolist()
            jjj = df.juliday.tolist()
            
            
            dvv_n=[]
            dvv_p=[]
            coef_n=[]
            coef_p=[]
            level=[]
            jday=[]
            new_dvv_p = []
            new_dvv_n = []
            new_level_p = []
            new_level_n = []
            new_jday_p = []
            new_jday_n = []
            new_coef_p = []
            new_coef_n = []
            new_dvv_p2 = []
            new_dvv_n2 = []
            new_level_p2 = []
            new_level_n2 = []
            new_jday_p2 = []
            new_jday_n2 = []
            new_coef_p2 = []
            new_coef_n2 = []
            LIM = 0.12
            a = 0
            b = 0
            c = 0
            d = 0
            for number in range(len(jjj)):
                if lll[number]==0:
                    break
                dvv_n.append(dn[number])
                dvv_p.append(dp[number])
                coef_n.append(cncn[number])
                coef_p.append(cpcp[number])
                level.append(lll[number])
                jday.append(jjj[number])
            #==========================for dvv_p=========================
            Xi = np.array(level)
            Yi = np.array(dvv_p)
            def func(p,x):
                k,b = p
                return k*x+b
            def error(p,x,y):
                return func(p,x)-y
            p0 = [30,30]
            Para = leastsq(error,p0,args=(Xi,Yi))
            kp1,bp1 = Para[0]
            coeff1_p,p=stats.pearsonr(dvv_p,level)
            #========================ANOVA============================
            yt_list_p = []
            yn_list_p = []            
            for i in range(len(level)):
                yn = kp1*level[i]+bp1 #理論值
                yn_list_p.append(yn) #理論值
                yt = (dvv_p[i]-yn) #residual
                yt_list_p.append(yt) #residual         
            # STDp=np.std(dvv_p)
            STDp=np.std(yn_list_p)
            # ========================first outlier====================
            for i in range(len(yt_list_p)):
                if abs(yt_list_p[i]) > 6*STDp:
                    a+=1
                    print('===',i,'===')
                else:
                    new_dvv_p.append(dvv_p[i])
                    new_level_p.append(level[i])
                    new_jday_p.append(jday[i])
                    new_coef_p.append(coef_p[i])
            Xi_1 = np.array(new_level_p)
            Yi_1 = np.array(new_dvv_p)
            Para = leastsq(error,p0,args=(Xi_1,Yi_1))
            kp2,bp2 = Para[0]
            coeff2_p,p=stats.pearsonr(new_dvv_p,new_level_p)
            #========================ANOVA============================
            new_yt_list_p = []
            new_yn_list_p = []
            for i in range(len(new_level_p)):
                yn = kp2*new_level_p[i]+bp2 #理論值
                new_yn_list_p.append(yn) #理論值
                yt = (new_dvv_p[i]-yn) #residual
                new_yt_list_p.append(yt) #residual
            STDp2=np.std(new_yn_list_p)
            # ========================second outlier====================
            for i in range(len(new_yn_list_p)):
                if abs(new_yt_list_p[i]) > 6*STDp2:
                    c+=1
                    print('----',i,'----')
                else:
                    new_dvv_p2.append(new_dvv_p[i])
                    new_level_p2.append(new_level_p[i])
                    new_jday_p2.append(new_jday_p[i])
                    new_coef_p2.append(new_coef_p[i])
            Xi_1 = np.array(new_level_p2)
            Yi_1 = np.array(new_dvv_p2)
            Para = leastsq(error,p0,args=(Xi_1,Yi_1))
            kp3,bp3 = Para[0]
            coeff3_p,p=stats.pearsonr(Yi_1,Xi_1)
            # # ========================plot=============================
            plt.rcParams['figure.figsize'] =15,15
            ax = subplot(221)
            aaa=plt.scatter(level,dvv_p,lw=0.5,c=coef_p,cmap='rainbow',vmin=0.0, vmax=1)
            plt.plot(level,yn_list_p,'k',lw = 3)
            plt.ylim(-LIM,LIM)
            plt.xlim(253,272)
            plt.xlabel('dv/v ',fontsize=20)
            plt.ylabel('Groundwater level (m)',fontsize=20)
            # plt.text(-0.09,271,'Negative',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            ax = plt.gca()
            ax.xaxis.set_major_locator(MultipleLocator(2))
            
            plt.subplot(222)
            plt.subplots_adjust(wspace=0.12) 
            plt.scatter(new_level_p,new_dvv_p,lw=0.5,c=new_coef_p,cmap='rainbow',vmin=0.0, vmax=1)
            plt.xlabel('Groundwater level (m)',fontsize=20)
            plt.yticks(fontsize=12)
            plt.plot(new_level_p,new_yn_list_p,'k',lw = 3)
            plt.ylim(-LIM,LIM)
            plt.xlim(253,272)
            plt.xlabel('dv/v',fontsize=20)
            # plt.text(0.05,271,'Positive',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
            plt.xticks(fontsize=15)
            ax = plt.gca()
            ax.xaxis.set_major_locator(MultipleLocator(2))
            
            plt.suptitle(pair+'\n'+' stk '+str(stkdays)+' days'+'  w='+window,fontsize=20)
            plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
            cax = plt.axes([0.81, 0.5, 0.02, 0.41])
            cbr=plt.colorbar(aaa, cax=cax)
            cbr.set_label('Coefficient',fontsize=22)   
            plt.show()
            # #==========================for dvv_n=========================
            Xi = np.array(level)
            Yi = np.array(dvv_n)
            p0 = [30,30]
            Para = leastsq(error,p0,args=(Xi,Yi))
            kn1,bn1 = Para[0]
            coeff1_n,p=stats.pearsonr(dvv_n,level)
            #========================ANOVA============================
            # STDn = 0
            yt_list_n = []
            yn_list_n = []
            for i in range(len(level)):
                yn = kn1*level[i]+bn1 #理論值
                yt = (dvv_n[i]-yn) #residual
                # STDn += (dvv_n[i]-np.mean(dvv_n))**2/len(dvv_n)
                yt_list_n.append(yt) #residual
                yn_list_n.append(yn) #理論值
            # STDn=np.std(yn_list_n)
            STDn=np.std(dvv_n)
            #========================first outlier====================
            for i in range(len(yt_list_n)):
                if abs(yt_list_n[i]) > 6*STDn :
                    b+=1
                    print('KKK',i,'KKK')
                else:
                    new_dvv_n.append(dvv_n[i])
                    new_level_n.append(level[i])
                    new_jday_n.append(jday[i])
                    new_coef_n.append(coef_n[i])
            Xi_1 = np.array(new_level_n)
            Yi_1 = np.array(new_dvv_n)
            Para = leastsq(error,p0,args=(Xi_1,Yi_1))
            kn2,bn2 = Para[0]
            coeff2_p,p=stats.pearsonr(new_dvv_n,new_level_n)
            #========================ANOVA============================
            new_yt_list_n = []
            new_yn_list_n = []
            for i in range(len(new_level_n)):
                yn = kn2*new_level_n[i]+bn2 #理論值
                new_yn_list_n.append(yn) #理論值
                yt = (new_dvv_n[i]-yn) #residual
                new_yt_list_n.append(yt) #residual
            STDn2=np.std(new_yn_list_n)
            # # ========================plot=============================
            # plt.rcParams['figure.figsize'] =15,15
            # ax = subplot(221)
            # aaa=plt.scatter(level,dvv_n,lw=0.5,c=coef_n,cmap='rainbow',vmin=0.0, vmax=1)
            # plt.plot(level,yn_list_n,'k',lw = 3)
            # plt.ylim(-LIM,LIM)
            # plt.xlabel('dv/v ',fontsize=20)
            # plt.ylabel('Groundwater level (m)',fontsize=20)
            # # plt.text(-0.09,271,'Negative',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
            # plt.xticks(fontsize=15)
            # plt.yticks(fontsize=15)
            # ax = plt.gca()
            # ax.xaxis.set_major_locator(MultipleLocator(2))
            
            # plt.subplot(222)
            # plt.subplots_adjust(wspace=0.12) 
            # plt.scatter(new_level_n,new_dvv_n,lw=0.5,c=new_coef_n,cmap='rainbow',vmin=0.0, vmax=1)
            # plt.xlabel('Groundwater level (m)',fontsize=20)
            # plt.yticks(fontsize=12)
            # plt.plot(new_level_n,new_yn_list_n,'k',lw = 3)
            # plt.ylim(-LIM,LIM)
            # # plt.xlim(253,272)
            # plt.xlabel('dv/v',fontsize=20)
            # # plt.text(0.05,271,'Positive',fontsize=18,bbox=dict(facecolor='pink', alpha=0.7))
            # plt.xticks(fontsize=15)
            # ax = plt.gca()
            # ax.xaxis.set_major_locator(MultipleLocator(2))
            
            # plt.suptitle(pair+'\n'+' stk '+str(11)+'NNNNN'+' days'+'  w='+window,fontsize=20)
            # plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
            # cax = plt.axes([0.81, 0.5, 0.02, 0.41])
            # cbr=plt.colorbar(aaa, cax=cax)
            # cbr.set_label('Coefficient',fontsize=22)               
            #====================make new csv=========================
            dfnn=pd.DataFrame({'juliday_n':new_jday_n,
                              'waterlevel_n':new_level_n,
                                'dvv_n': new_dvv_n,
                                'coeff_n': new_coef_n,
                                'residual_n':new_yt_list_n,
                                'yfunction_n':new_yn_list_n})
            dfpp=pd.DataFrame({'juliday_p':new_jday_p,
                                'waterlevel_p':new_level_p,
                                'dvv_p':new_dvv_p,
                                'coeff_p':new_coef_p,
                                'residual_p':new_yt_list_p,
                                'yfunction_p':new_yn_list_p })
            out = pd.concat([dfpp,dfnn],axis = 1)
                
            # out.to_csv('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'_'+window+'_bp'+HZ+'_outlier.csv')
            # print('DONE for '+pair+'_'+window+'_bp'+HZ+'_outlier.csv')