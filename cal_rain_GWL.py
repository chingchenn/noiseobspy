# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:54:12 2020

@author: grace
"""


import numpy as np
import pandas as pd
from scipy import stats
import matplotlib as mpl
from obspy import UTCDateTime
import matplotlib.pyplot as plt
from scipy import fftpack
from pandas.core.frame import DataFrame
from matplotlib.dates import (YearLocator, MONTHLY,DateFormatter,AutoDateLocator)


# rainfile='D:/2020summer/CHS/Chihshang_prep_finish/'
# newdate=pd.DataFrame()
# newprep=pd.DataFrame()
# for j,jjj in enumerate(sorted(glob.glob(rainfile+'/*.csv'))):
#     newrain=[]
#     beginUTC=[]
#     endUTC=[]
#     UTClist=[]
#     rainlist=[]
#     newUTC=[]
#     yymm=(jjj.rsplit('_',1)[1]).rsplit('.',1)[0]
#     if int(yymm) >=2013 and int(yymm) <=2021:
#         # print(yymm)
#         df=pd.read_csv(jjj, header= 0, encoding= 'unicode_escape')
#         UTC=np.array(df.date).tolist()
#         rain=np.array(df.prep)
#         rainlist.append(rain)
#         totalrain=0;kkk=0
#         for i,date in enumerate(UTC):
#             if rain[i]<0:
#                 rain[i]=0
#             yyyy1=int(str(date)[0:4])
#             mm1=int(str(date)[4:6])
#             dd1=int(str(date)[6:8])
#             date3=UTCDateTime(year=yyyy1,month=mm1,day=dd1)
#             # print(date3)
#             # newUTC.append(date3)
#             UTC2=str(date3.year)+'/'+str(date3.julday)
#             print(UTC2)
#             newUTC.append(UTC2)
#             ddd=pd.DataFrame(newUTC)
#             ppp=pd.DataFrame(rain)
        
#         newdate = pd.concat([newdate,ddd],axis = 0)
#         newprep = pd.concat([newprep,ppp],axis = 0)
#         newkkk=pd.concat([newdate,newprep],axis = 1)
        
#         newkkk.to_csv(rainfile+'daydata.csv')
rainfile='D:/2020summer/CHS/Chihshang_prep_finish/daydata.csv'
df=pd.read_csv(rainfile, encoding= 'unicode_escape')
# df = df.dropna() 
water = np.array(df.GWL).tolist()
rain = np.array(df.rainfall).tolist()
date = df.date
coeffw_p,p=stats.pearsonr(water,rain)
x=np.linspace(-1140,1140,2281)

# def normalize(v):
#     norm = np.linalg.norm(v)
#     if norm == 0: 
#         return v
#     return v / norm

# water = normalize(water)
# rain = normalize(rain)
# plt.xticks([])
# plt.scatter(x,water)
# plt.scatter(x,rain)
# plt.show()
plt.rcParams['figure.figsize']=15,10
def cxcorr(a,v):
    nom = np.linalg.norm(a[:])*np.linalg.norm(v[:])
    return fftpack.irfft(fftpack.rfft(a)*fftpack.rfft(v[::-1]))/nom
n = cxcorr(water,rain)
plt.plot(n)