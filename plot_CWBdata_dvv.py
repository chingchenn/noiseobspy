# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 14:25:02 2020

@author: grace
"""


##用來畫圖的程式
##把天氣資料跟速度變化量資料都帶進去，會跟論文中的圖長很像，只是還沒做dv/v的平均
import csv
import glob
import time
import math
import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats
import matplotlib as mpl
from obspy import UTCDateTime
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from CCF_functions import whiten,normalize
from matplotlib.dates import (YearLocator, MONTHLY,DateFormatter,AutoDateLocator)



# ##=================================氣象局資料==================================
tttdate = [];ttt = [];UTCttt = []
# file = 'D:/2020summer/池上/TEMPETURE/daydata/all.csv'
file = 'D:/2020summer/池上/TEMPETURE/monthdata/tt.csv'
df = pd.read_csv(file)
date = df['date-time']
tem = df['tempeture']
hPa = df['hPa']
prep = df['rain prep']
vel = df['wind vel']
for i in range (len(tem)):
    if tem[i]==str('...'):
        tem[i]=20
    if hPa[i]==str('...'):
        hPa[i] = 980
    if prep[i]==str('...'):
        prep[i]=0
    elif prep[i]==str('...') or prep[i]==str('/') :
        prep[i]=0  
    if vel[i]==str('...') or vel[i] ==str('X'):
        vel[i]=0
tem = list(map(float, tem))
hPa = list(map(float, hPa))
prep = list(map(float, prep))
vel = list(map(float, vel))
for UUU in date:
    year = UUU.rsplit('-',3)[0]
    month=UUU.rsplit('-',3)[1]
    day=UUU.rsplit('-',3)[2].rsplit(' ',2)[0]
    UTC=dt.datetime(year=int(year), month=int(month), day=int(day))
    jjj = time.strptime(year+'.'+month+'.'+day, "%Y.%m.%d").tm_yday
    UTCttt.append(UTC)
##=================================地下水=================================
waterpath='D:/2020summer/池上/池上地下水.csv'
grounddate=[];groundwater=[];UTCground=[]
with open (waterpath,newline='') as wfile:
    rows=list(csv.reader(wfile,delimiter=','))
    for row in rows[1:]:
        grounddate.append(row[0])
        groundwater.append(float(row[1]))
    for UUU in grounddate:
        year=UUU.rsplit('/',3)[0]
        month=UUU.rsplit('/',3)[1]
        day=UUU.rsplit('/',3)[2]
        UTC=dt.datetime(year=int(year), month=int(month), day=int(day),fold=1)
        UTCground.append(UTC)


####====================雨量==========================
formatter = DateFormatter('20%y')
newrain=[]
newUTC=[]
path = 'D:/2020summer/CHS/Chihshang_prep_finish/'
for i,csvfile in enumerate(sorted(glob.glob(path+'*week.csv'))):
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
            
listrr = []
uu = np.mean(newrain)
uun = np.std(newrain)
for i in range(len(newrain)):
    r1 = (newrain[i]-uu)/uun
    listrr.append(abs(r1)) 
    
    
###=============================================================
YEAR='2013-2016'
pair = 'CHS5-CHS4'
window ='4_8'
HZ = '1_4'

##=================================   dv/v資料   =================================
refile = 'D:/2020summer/CHS/stretching/count/CGF11days/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'outlier_data.csv'
df1 = pd.read_csv(refile)
JJJp=df1.date_p;tp=df1.tempeture_p
wp=df1.waterlevel_p;vvp=df1.dvv_p
cp=df1.coeff_p;rp=df1.residual_p
yfp=df1.yfunction_p;hp=df1.hPa_p
# prep=df1['rain prep_p'];vp=df1['wind vel_p']
JJJn=df1.date_n;tn=df1.tempeture_n
wn=df1.waterlevel_n;vvn=df1.dvv_n
cn=df1.coeff_n;rn=df1.residual_n
yfn=df1.yfunction_n;hn=df1.hPa_n
pren=df1['rain prep_n'];vn=df1['wind vel_n']

r_n = list(map(float, rn))
r_p = list(map(float, rp))
DAY_p=[];DAY_n=[];rp = [];rn = [];yp=[];yn=[]
waterp=[];watern=[];dvp=[];dvn=[];ccp=[];ccn=[]
temp = [];hPap=[];prepp=[];velp=[]
# temn = [];hPan=[];prepn=[];veln=[]

for i , UTC in enumerate(JJJp):
    if type(UTC) ==float:
        break
    date3=UTCDateTime(UTC)
    UTC1=dt.datetime(year=date3.year, month=date3.month, day=date3.day,fold=1)
    DAY_p.append(UTC1)
    rp.append(r_p[i])
    yp.append(yfp[i])
    waterp.append(wp[i])
    dvp.append(vvp[i])
    ccp.append(cp[i])
    temp.append(tp[i])
    hPap.append(hp[i])
    # prepp.append(prep[i])
    # velp.append(vp[i])
for i , UTC in enumerate(JJJn):
    if type(UTC) ==float:
        break
    date3=UTCDateTime(UTC)
    UTC1=dt.datetime(year=date3.year, month=date3.month, day=date3.day,fold=1)
    DAY_n.append(UTC1)
    rn.append(r_n[i])
    yn.append(yfn[i])
    watern.append(wn[i])
    dvn.append(vvn[i])
    ccn.append(cn[i])
    # temn.append(tn[i])
    # hPan.append(hn[i])
    # prepn.append(pren[i])
    # veln.append(vn[i])
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

rp = normalize(rp)
rn = normalize(rn)

# groundwater = normalize(groundwater)
prep = normalize(prep)


###
plt.rcParams['figure.figsize']=23,20
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(UTCttt,tem,c='blue',lw=2,ls='-',label = 'tempeture')
ax1.set_xlim(dt.datetime(2014, 3, 1, 0, 0),dt.datetime(2015, 3, 1, 0, 0))
ax1.set_ylabel('tempeture',c='blue',fontsize=20)
ax1.tick_params(axis='y', labelcolor='blue')
ax = plt.gca() 
ax2 = plt.twinx()
ax2.plot(UTCttt,vel,lw = 2,c='r',label = 'wind speed')
ax2.set_ylabel('wind speed',c='r',fontsize=20)
ax3=plt.twinx()
ax3.plot(UTCttt,hPa,lw=4,c='g',label = 'air pressure')
ax3.set_ylabel('hPa',c='g',fontsize=30)
ax4=plt.twinx()
ax4.bar(UTCttt,prep,width=2,color = 'gray',label = 'rainfall')
# ax4.plot(UTCttt,prep,c='k')
ax4.set_ylim(0,1)
# ax5=plt.twinx()
# ax5.plot(UTCground,groundwater,lw=4,c='k',label = 'groundwater')
# ax5.set_ylabel('groundwater',c='k',fontsize=30)
ax6=plt.twinx()
ax6.plot(DAY_p,rp,c='pink',lw=6,label = 'postive')
# ax6.set_ylim(-0.1,0.1)
# ax6.set_ylabel('groundwater',c='k',fontsize=30)
ax7=plt.twinx()
ax7.plot(DAY_n,rn,c='k',lw=6,label = 'negative')
# ax7.set_ylim(-0.1,0.1)
# ax7.set_ylabel('groundwater',c='k',fontsize=30)
# ax2.legend(fontsize=12)
# ax3.legend(fontsize=12)
# ax4.legend(fontsize=12)
plt.show()