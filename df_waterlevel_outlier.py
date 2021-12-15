#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 09:47:50 2020

@author: teach
"""

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import leastsq
import sys, obspy, os,glob
import datetime as dt
import matplotlib as mpl
import matplotlib.dates as mdates
from obspy.core import UTCDateTime
from matplotlib.dates import (YEARLY, DateFormatter,date2num,num2date,
                              rrulewrapper, RRuleLocator, drange)
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
pair='CHS5-CHS2'
window='3_7'
YEAR='2013-2016'
# stkdays=5
HZ = '1_4'
filename='D:/2020summer/CHS/stretching/count/CGF11days/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'out.csv'
df=pd.read_csv(glob.glob(filename)[0])
dt_n=df.dvv_n
dt_p=df.dvv_p
coef_n=df.coeff_n
coef_p=df.coeff_p
level=df.waterlevel
jday = df.juliday
yt_list = []

yto_p = []
new_yt_p_2= []
dto_p = []
new_dt_p = []
new_dt_p_2 = []
levelo_p = []
new_level_p = []
new_level_2_p = []
jdayo_p = []
new_jday_p = []
new_jday_2_p = []
coefo_p = []
new_coef_p = []
new_coef_2_p = []
a = 0
b = 0
c = 0
d = 0
e = 0
f = 0

#===================point out of our consider===============
for i in range(len(level)):
    # if dt_p[i]<-0.2 or dt_p[i]>0.2 or level[i] >265.5:
    if dt_p[i]<-0.1 or dt_p[i]>0.1 :
        a+=1
    else:
        dto_p.append(dt_p[i])
        levelo_p.append(level[i])
        jdayo_p.append(jday[i])
        coefo_p.append(coef_p[i])
#==========================for dt_p=========================
Xi = np.array(levelo_p)
Yi = np.array(dto_p)
def func(p,x):
    k,b = p
    return k*x+b
def error(p,x,y):
    return func(p,x)-y
p0 = [30,30]
Para = leastsq(error,p0,args=(Xi,Yi))
k1,b1 = Para[0]
#========================ANOVA============================
STD = 0
for i in range(len(levelo_p)):
    yn = k1*levelo_p[i]+b1
    yt = (dto_p[i]-yn)**2
    STD += (dto_p[i]-np.mean(dto_p))**2/len(dto_p)
    yt_list.append(yt)
#========================first outlier====================
STD = np.sqrt(STD)
for i in range(len(yt_list)):
      if yt_list[i] > 20*STD:
        b+=1
        # print('===',i,'===')
      else:
        new_dt_p.append(dto_p[i])
        new_level_p.append(levelo_p[i])
        new_jday_p.append(jdayo_p[i])
        new_coef_p.append(coefo_p[i])
Xi_1 = np.array(new_level_p)
Yi_1 = np.array(new_dt_p)
Para = leastsq(error,p0,args=(Xi_1,Yi_1))
k2,b2 = Para[0]
#========================ANOVA============================
STD_2 = 0
yp_list = []
for i in range(len(new_dt_p)):
    yt = k2*new_level_p[i]+b2
    yp = (new_dt_p[i]-yt)**2
    STD_2 += (new_dt_p[i]-np.mean(new_dt_p))**2/len(new_dt_p)
    yp_list.append(yp)
#========================second outlier====================
STD_2 = np.sqrt(STD_2)
for i in range(len(yp_list)):
      if yp_list[i] > 20*STD_2:
        c+=1
        # print('---',i,'---')
      else:
        new_yt_p_2.append(yp_list[i])  
        new_dt_p_2.append(new_dt_p[i])
        new_level_2_p.append(new_level_p[i])
        new_jday_2_p.append(new_jday_p[i])
        new_coef_2_p.append(new_coef_p[i])
Yi_2 = np.array(new_dt_p_2)
Xi_2 = np.array(new_level_2_p)
Para = leastsq(error,p0,args=(Xi_2,Yi_2))
k3,b3 = Para[0]


y = k3*Xi_2+b3
new_yt_p_2 = y.tolist()
SSr2 = 0
STD_3 = 0
STD_4 = 0
level_mean = np.mean(new_level_2_p)
dt_mean = np.mean(new_dt_p_2)
for i in range(len(new_yt_p_2)):
      SSr2 += (new_yt_p_2[i]-level_mean)**2
      STD_3+= (new_level_2_p[i]-level_mean)**2 
      STD_4+= (new_dt_p_2[i]-dt_mean)**2
    
Rp = (SSr2/STD_3)
cccp = np.sqrt(Rp)
   

# # # ========================plot=============================
# filename= 'D:/2020summer/summer2020/stretching/count/new/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'w.csv'
# df=pd.read_csv(glob.glob(filename)[0])
# dt_n=df.shift_n
# dt_p=df.shift_p
# coef_n=df.coeff_n
# coef_p=df.coeff_p
# level_n=df.waterlevel_n
# level_p=df.waterlevel_p
# jday_n=df.juliday_n
# jday_p=df.juliday_p
# yfu_n = df.yfunction_n
# yfu_p = df.yfunction_p
# plt.rcParams['figure.figsize'] =15,15
# plt.subplot(222)
# plt.subplots_adjust(wspace=0.12) 
# plt.scatter(level_p,-dt_p,lw=0.5,c=coef_p,cmap='Reds',vmin=0.4, vmax=1)
# plt.plot(yfu_p,-dt_p,'k',lw = 3)
# plt.ylim(-0.06,0.06)
# plt.xlim(250,272)
# plt.xlabel('Groundwater level (m)',fontsize=20)
# plt.yticks([])

# #===========================================================
# pair='CHS5-CHS2'
# window='2.5_5'
# YEAR='2013-2016'
# stkdays=5
# NET_PATH='/run/user/1000/gvfs/sftp:host=140.109.81.176'
# # NET_PATH='/home/teach/CHS/csv'
# filename= NET_PATH+'/home/summer/stretching/count/02_CGF5days/'+pair+'/'+pair+'_'+YEAR+'_w'+window+'_stk'+str(stkdays)+'_water_v3.csv'
# # filename= NET_PATH+'/'+pair+'_'+YEAR+'*_water_v2.csv'
# df=pd.read_csv(glob.glob(filename)[0])
dt_n=df.dvv_n
dt_p=df.dvv_p
coef_n=df.coeff_n
coef_p=df.coeff_p
level=df.waterlevel
jday = df.juliday
yt_list = []
yto_n = []
new_yt_n= []
new_yt_n_2= []
dto_n = []
new_dt_n = []
new_dt_n_2 = []
levelo_n = []
new_level_n = []
new_level_2_n = []
jdayo_n = []
new_jday_n = []
new_jday_2_n = []
ceofo_n = []
new_coef_n = []
new_coef_2_n = []
#===================point out of our consider===============
for i in range(len(level)):
    if dt_n[i]<-0.1 or dt_n[i]>0.1:
        d+=1
        # print('===',i,'nout===')
    else:
        dto_n.append(dt_n[i])
        levelo_n.append(level[i])
        jdayo_n.append(jday[i])
        ceofo_n.append(coef_n[i])
#==========================for dt_n=========================
Xi = np.array(levelo_n)
Yi = np.array(dto_n)
p0 = [30,30]
Para = leastsq(error,p0,args=(Xi,Yi))
k1,b1 = Para[0]
#========================ANOVA============================
STD = 0
yt_list = []
for i in range(len(levelo_n)):
    yn = k1*levelo_n[i]+b1
    yt = (dto_n[i]-yn)**2
    STD += (dto_n[i]-np.mean(dto_n))**2/len(dto_n)
    yt_list.append(yt)
#========================first outlier====================
STD = np.sqrt(STD)
for i in range(len(yt_list)):
      if yt_list[i] > 20*STD:
        e+=1
        # print('===',i,'===')
      else:
        new_yt_n.append(yt_list[i])
        new_dt_n.append(dto_n[i])
        new_level_n.append(levelo_n[i])
        new_jday_n.append(jdayo_n[i])
        new_coef_n.append(ceofo_n[i])
Xi_1 = np.array(new_level_n)
Yi_1 = np.array(new_dt_n)
Para = leastsq(error,p0,args=(Xi_1,Yi_1))
k2,b2 = Para[0]
#========================ANOVA============================
STD_2 = 0
yp_list = []
for i in range(len(new_dt_n)):
    yt = k2*new_level_n[i]+b2
    yp = (new_dt_n[i]-yt)**2
    STD_2 += (new_dt_n[i]-np.mean(new_dt_n))**2/len(new_dt_n)
    
    yp_list.append(yp)
#========================second outlier====================
STD_2 = np.sqrt(STD_2)
for i in range(len(yp_list)):
      if yp_list[i] > 60*STD_2:
        f+=1
        # print('---',i,'---')
      else:
        new_yt_n_2.append(yp_list[i])  
        new_dt_n_2.append(new_dt_n[i])
        new_level_2_n.append(new_level_n[i])
        new_jday_2_n.append(new_jday_n[i])
        new_coef_2_n.append(new_coef_n[i])
Yi_2 = np.array(new_dt_n_2)
Xi_2 = np.array(new_level_2_n)
Para = leastsq(error,p0,args=(Xi_2,Yi_2))
k3,b3 = Para[0]
y = k3*Xi_2+b3
new_yt_n_2 = y.tolist()
SSr2 = 0
STD_3 = 0
STD_4 = 0
# level_mean = np.mean(new_level_2_n)
# dt_mean = np.mean(new_dt_n_2)
# NPTS = len(new_yt_n_2)
# for i in range(len(new_yt_n_2)):
#     SSr2 += (new_yt_n_2[i]-level_mean)*(new_dt_n_2[i]-dt_mean)  
#     STD_3+= (new_level_2_n[i]-level_mean)**2 
#     STD_4+= (new_dt_n_2[i]-dt_mean)**2
    
# Rn = -(SSr2/STD_3/STD_4)
# ccc = np.sqrt(Rn)
# #====================make new csv=========================
df=pd.DataFrame({'juliday_n':new_jday_2_n,
                  'waterlevel_n':new_level_2_n,
                    'shift_n': new_dt_n_2,
                    'coeff_n': new_coef_2_n,
                    'yfunction_n':new_yt_n_2})
df1=pd.DataFrame({'juliday_p':new_jday_2_p,
                    'waterlevel_p':new_level_2_p,
                    'shift_p':new_dt_p_2,
                    'coeff_p':new_coef_2_p,
                    'yfunction_p':new_yt_p_2 })
df2 = pd.DataFrame({'original_days':len(jday),'limit_p':a,'first_std_p':b,'sec_std_p':c,
                    'limit_n':d,'first_std_n':e,'sec_std_n':f},index = [0])
df3 = pd.DataFrame({})
out = pd.concat([df,df1],axis = 1)
# out.to_csv('D:/2020summer/summer2020/stretching/count/new/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'out.csv')
# # # ========================plot=============================
x = np.linspace(round(min(dto_n),2),round(max(dto_n),2))
y = k1*x+b1
plt.plot(x,y,'b',lw = 7)
plt.plot(level,dt_n,'bo')
# plt.xlim(-0.15,0.05)
plt.ylabel('dt(s)')
plt.xlabel('water level(m)')


y = k2*x+b2
plt.plot(x,y,'k',lw = 7)
# plt.xlim(-0.15,0.05)
plt.xlabel('dt(s)')
plt.ylabel('water level(m)')
plt.plot(new_dt_n,new_level_n,'ko')


y = k3*x+b3
plt.plot(new_dt_n_2,new_yt_n_2,'g',lw = 7)
plt.xlabel('dt(s)')
plt.ylabel('water level(m)')
# plt.xlim(-0.15,0.05)
plt.plot(new_dt_n_2,new_level_2_n,'go')
plt.show()

# fig, ax = plt.subplots(nrows=2,ncols=1,gridspec_kw={'height_ratios':[1,1]})

# filename= 'D:/2020summer/summer2020/stretching/count/new/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'out.csv'
# df=pd.read_csv(glob.glob(filename)[0])
# dt_n=df.shift_n
# dt_p=df.shift_p
# coef_n=df.coeff_n
# coef_p=df.coeff_p
# level_n=df.waterlevel_n
# level_p=df.waterlevel_p
# jday_n=df.juliday_n
# jday_p=df.juliday_p
# yfu_n = df.yfunction_n
# yfu_p = df.yfunction_p

# ax = subplot(221)
# aaa=plt.scatter(level_n,dt_n,lw=0.5,c=coef_n,cmap='Reds',vmin=0.4, vmax=1)
# plt.plot(yfu_n,dt_n,'k',lw = 3)
# plt.ylim(-0.06,0.06)
# plt.xlim(250,272)
# plt.ylabel('dv/v ',fontsize=20)
# plt.xlabel('Groundwater level (m)',fontsize=20)
# plt.text(254,-0.1,'r = ')



# plt.suptitle(pair+'\n'+YEAR+' stk '+str(stkdays)+' days'+'  w='+window,fontsize=20)

# plt.subplots_adjust(bottom=0.1, right=0.78, top=0.9)
# cax = plt.axes([0.81, 0.5, 0.02, 0.41])
# cbr=plt.colorbar(aaa, cax=cax)
# cbr.set_label('Coefficient',fontsize=22)           
# plt.savefig('/home/teach/Poster/'+pair+'_'+'w'+window+'iiiii.pdf')

# print('p=',a,b,c,a+b+c,len(jday),(a+b+c)/len(jday))
# print('n=',d,e,f,d+e+f,len(jday),(d+e+f)/len(jday))
# print(Rp,Rn)
# print(ccc)


