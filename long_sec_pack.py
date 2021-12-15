# -*- coding: utf-8 -*-
"""
Created on Sun May 30 14:41:56 2021

@author: grace
"""


import glob
import numpy as np
import pandas as pd
from obspy.core import UTCDateTime

pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2','CHS5-CHS1']
way = ['tn8-n1f1-3','tn8-n1f3-5','tn8-n1f5-7','tn9-n2f1-3','tn9-n2f3-5','tn9-n2f5-7',
        'tn10-n3f1-3','tn10-n3f3-5','tn10-n3f5-7','tn11-n4f1-3','tn11-n4f3-5',
        'tn11-n4f5-7','tn12-n5f1-3','tn12-n5f3-5','tn12-n5f5-7']
wattt = ['tp1-p8f1-3','tp1-p8f3-5','tp1-p8f5-7','tp2-p9f1-3','tp2-p9f3-5','tp2-p9f5-7',
           'tp3-p10f1-3','tp3-p10f3-5','tp3-p10f5-7','tp4-p11f1-3','tp4-p11f3-5','tp4-p11f5-7'
           ,'tp5-p12f1-3','tp5-p12f3-5','tp5-p12f5-7']
# pair_list = ['CHS5-CHS4']
# way = ['tn8-n1f3-5']
# wattt = ['tp1-p8f3-5']
# way = ['tn8-n1f1-3','tn8-n1f3-5','tn8-n1f5-7','tn9-n2f1-3','tn9-n2f3-5','tn9-n2f5-7',
#         'tn10-n3f1-3','tn10-n3f3-5','tn10-n3f5-7','tn11-n4f1-3','tn11-n4f3-5',
#         'tn11-n4f5-7','tn12-n5f1-3','tn12-n5f3-5','tn12-n5f5-7']
# wattt = ['tp1-p8f3-5','tp1-p8f5-7','tp2-p9f1-3','tp2-p9f3-5','tp2-p9f5-7',
#           'tp3-p10f1-3','tp3-p10f3-5','tp3-p10f5-7','tp4-p11f1-3','tp4-p11f3-5','tp4-p11f5-7'
#           ,'tp5-p12f1-3','tp5-p12f3-5','tp5-p12f5-7']
for pair in pair_list:
    for www , ddd in enumerate(way): 
        kkkn=pd.DataFrame()
        DIR='D:/2020summer/CHS/stretching/long_sec/'+way[www]+'/'+pair+'/*eps4'
        for i , ddd in enumerate(glob.glob(DIR)):
            tempnnn=glob.glob(DIR)[i]
            file=pd.read_csv(glob.glob(tempnnn)[0],sep = '\s+',header=None)
            jday = file[0]
            yyyy = tempnnn.rsplit('/',4)[-1].rsplit('.',2)[1]
            sta= tempnnn.rsplit('/',4)[-1].rsplit('\\',1)[0]
            juliday_list=[]
            for j in range(len(file[0])):
                yyyyddd = str(yyyy)+'/'+str(file[0][j])
                juliday_list.append(yyyyddd)
            juliday_list = pd.DataFrame({'jday':juliday_list})
            lsit1= pd.DataFrame({'ep1_n':file[1]})
            lsit2= pd.DataFrame({'ccc1_n':file[2]})
            lsit3= pd.DataFrame({'ep2_n':file[3]})
            lsit4= pd.DataFrame({'ccc2_n':file[4]})
            lsit5= pd.DataFrame({'ep3_n':file[5]})
            lsit6= pd.DataFrame({'ccc3_n':file[6]})
            nnn = pd.concat([juliday_list,lsit1,lsit2,lsit3,lsit4,lsit5,lsit6],axis=1)        
            # print(tempnnn)
            freq=way[www].rsplit('f',2)[-1]
            win =way[www].rsplit('n')[1]+way[www].rsplit('-')[1][1]
            # print(win)
            # nnn.to_csv('D:/2020summer/CHS/stretching/long_sec/'+pair+'/'+pair+'-'+yyyy+'-'+win+'-bp'+freq+'n.csv')
            kkkn=pd.concat([kkkn,nnn],axis=0)
        
            
        kkkp=pd.DataFrame()
        DIR='D:/2020summer/CHS/stretching/long_sec/'+wattt[www]+'/'+pair+'/*eps4'
        for i , ddd in enumerate(glob.glob(DIR)):
            tempppp=glob.glob(DIR)[i]
            file=pd.read_csv(glob.glob(tempppp)[0],sep = '\s+',header=None)
            jday = file[0]
            yyyy = tempppp.rsplit('/',4)[-1].rsplit('.',2)[1]
            sta= tempppp.rsplit('/',4)[-1].rsplit('\\',1)[0]
            juliday_list=[]
            for j in range(len(file[0])):
                yyyyddd = str(yyyy)+'/'+str(file[0][j])
                juliday_list.append(yyyyddd)
            juliday_list = pd.DataFrame({'jday':juliday_list})
            lsit1= pd.DataFrame({'ep1_p':file[1]})
            lsit2= pd.DataFrame({'ccc1_p':file[2]})
            lsit3= pd.DataFrame({'ep2_p':file[3]})
            lsit4= pd.DataFrame({'ccc2_p':file[4]})
            lsit5= pd.DataFrame({'ep3_p':file[5]})
            lsit6= pd.DataFrame({'ccc3_p':file[6]})
            ppp = pd.concat([juliday_list,lsit1,lsit2,lsit3,lsit4,lsit5,lsit6],axis=1)        
            # print(tempppp)
            freq=wattt[www].rsplit('f',2)[-1]
            win =wattt[www].rsplit('p')[1]+wattt[www].rsplit('-')[1].rsplit('f')[0].rsplit('p')[1]
            # ppp.to_csv('D:/2020summer/CHS/stretching/long_sec/'+pair+'/'+pair+'-'+yyyy+'-'+win+'-bp'+freq+'p.csv')
            kkkp=pd.concat([kkkp,ppp],axis=0)
            
        kkkall=pd.concat([kkkp,kkkn],axis=1)
        print(pair+'/'+pair+'-2013-2020-'+win+'-bp'+freq+'.csv')
        kkkall.to_csv('D:/2020summer/CHS/stretching/long_sec/'+pair+'/'+pair+'-2013-2020-'+win+'-bp'+freq+'.csv')

import datetime as dt
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] =17,9
pair_list = ['CHS5-CHS1','CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
# pair_list = ['CHS5-CHS4']
window_list = ['1-8','2-9','3-10','4-11','5-12']
HZ_list = ['1-3','3-5','5-7']
for pair in pair_list:
    for HZ in HZ_list:
        for window in window_list:
            csvpath='D:/2020summer/CHS/stretching/long_sec/'+pair+'/'+pair+'-2013-2020-'+window+'-bp'+HZ+'.csv'
            time=dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2021, 1, 1, 0, 0)
            if glob.glob(csvpath) ==[]:
                continue
            df = pd.read_csv(glob.glob(csvpath)[0])
            shift_n=df.ep1_n
            coeff_n=df.ccc1_n
            shift_n2=df.ep2_n
            coeff_n2=df.ccc2_n
            shift_n3=df.ep3_n
            coeff_n3=df.ccc3_n
            JJJ=list(df.jday)
            CGF_day_list=[]
            for i , UTC in enumerate(JJJ):
                yyyy=UTC.rsplit('/',1)[0]
                jjj=UTC.rsplit('/',1)[1]
                aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
                UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
                CGF_day_list.append(UUU)
                
            plt.axhline(y=0,color='lightgrey')
            aaa=plt.scatter(CGF_day_list,shift_n,c='r',s=10,label='1')
            plt.scatter(CGF_day_list,shift_n2,c='g',s=10,label='2')
            plt.scatter(CGF_day_list,shift_n3,c='b',s=10,label='3')
            plt.ylabel('negative -dv/v',fontsize=25)
            plt.legend(fontsize=20,loc = 4)
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=40)
            plt.title(pair+' window: '+window+' s bp freq: '+HZ+' hz negative side',fontsize=30)
            plt.xlim(time)
            plt.grid(axis='x')
            plt.tick_params(which='major', length=12,labelsize=20)
            # plt.savefig( 'D:/2020summer/CHS/stretching/long_sec/fig/'+pair+'-'+window+'-'+HZ+'n.jpg')
            # plt.cla()
            plt.show()
plt.rcParams['figure.figsize'] =17,9
for pair in pair_list:
    for HZ in HZ_list:
        for window in window_list:
            csvpath='D:/2020summer/CHS/stretching/long_sec/'+pair+'/'+pair+'-2013-2020-'+window+'-bp'+HZ+'.csv'
            time=dt.datetime(2013, 1, 1, 0, 0),dt.datetime(2021, 1, 1, 0, 0)
            if glob.glob(csvpath) ==[]:
                continue
            df = pd.read_csv(glob.glob(csvpath)[0])
            shift_p=df.ep1_p
            coeff_p=df.ccc1_p
            shift_p2=df.ep2_p
            coeff_p2=df.ccc2_p
            shift_p3=df.ep3_p
            coeff_p3=df.ccc3_p
            JJJ=list(df.jday)
            CGF_day_list=[]
            for i , UTC in enumerate(JJJ):
                yyyy=UTC.rsplit('/',1)[0]
                jjj=UTC.rsplit('/',1)[1]
                aaa=UTCDateTime(year=int(yyyy),julday=int(jjj))
                UUU=dt.datetime(year=int(yyyy),month=aaa.month,day=aaa.day)
                CGF_day_list.append(UUU)
                
            plt.axhline(y=0,color='lightgrey')
            aaa=plt.scatter(CGF_day_list,shift_p,c='r',s=10,label='1')
            plt.scatter(CGF_day_list,shift_p2,c='g',s=10,label='2')
            plt.scatter(CGF_day_list,shift_p3,c='b',s=10,label='3')
            plt.ylabel('positive -dv/v',fontsize=25)
            plt.legend(fontsize=20,loc = 4)
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=40)
            plt.title(pair+' window: '+window+' s bp freq: '+HZ+' hz positive side',fontsize=30)
            plt.xlim(time)
            plt.grid(axis='x')
            plt.tick_params(which='major', length=12,labelsize=20)
            # plt.savefig( 'D:/2020summer/CHS/stretching/long_sec/fig/'+pair+'-'+window+'-'+HZ+'p.jpg')
            # plt.cla()
            plt.show()