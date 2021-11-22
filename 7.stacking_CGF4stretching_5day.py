#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:50:56 2020

@author: wtl_st
"""


import os,glob
import datetime as dt
import matplotlib as mpl
from obspy import read,Trace
from obspy.core import UTCDateTime

date1 = dt.datetime(2012,12,31)
date2 = dt.datetime(2020, 9, 1)
delta= dt.timedelta(days=1)
dates= mpl.dates.drange(date1, date2, delta)

CCF_DIR='D:/2020summer/CHS/D03_CCF'
stkday=5
# pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2','CHS5-CHS1']
pair_list = ['CHS5-CHS1']
# pair_list = ['IT01-IT03','IT01-IT04','IT01-IT05','IT01-IT07','IT01-IT09','IT02-IT01','IT02-IT03','IT02-IT04','IT02-IT05','IT02-IT06','IT02-IT07','IT02-IT08','IT02-IT09','IT02-IT10',
#              'IT03-IT04','IT03-IT05','IT03-IT07','IT03-IT09','IT04-IT05','IT04-IT07','IT06-IT01','IT06-IT01','IT06-IT03','IT06-IT05','IT06-IT07','IT06-IT08','IT06-IT09','IT06-IT10',
#              'IT07-IT05','IT08-IT01','IT08-IT03','IT08-IT04','IT08-IT05','IT08-IT07','IT09-IT05','IT09-IT04','IT10-IT01','IT10-IT03','IT10-IT04','IT10-IT05','IT10-IT07','IT10-IT09']
for pair in pair_list:
    CGF_DIR='D:/2020summer/CHS/stretching/'+pair+'_CGF5days'
    if not os.path.isdir(CGF_DIR):
        os.makedirs(os.path.join(CGF_DIR))
    def strjjj(jjj):
        jjj=str(jjj)
        if len(jjj)==1:
            return '00'+jjj
        elif len(jjj)==2:
            return '0'+jjj
        else: return jjj
    
    for UTC in dates:
        UUU=UTCDateTime(mpl.dates.num2date(UTC))
        
        jjj=UUU.julday
        print(jjj)
        print('=================================')
        temp_stk=0;number=0
        for JJ in range(stkday):
            yyyy=UUU.year
            ccfjjj=jjj+JJ-4         ##-----------------------------------have to adjust
            
            if yyyy != 2020 and jjj == 365 :
                if JJ ==3 : newyyyy=yyyy+1 ;  newjjj=1
                elif JJ ==4 : newyyyy=yyyy+1 ; newjjj=2
                else: newyyyy=yyyy ;newjjj=ccfjjj
            elif yyyy != 2020 and jjj == 364:
                if JJ ==4 : newyyyy=yyyy+1 ; newjjj=1
                else: newyyyy=yyyy ;newjjj=ccfjjj
            elif yyyy!=2017 and jjj==1 :
                if JJ==0 : newyyyy=yyyy-1 ; newjjj=364
                elif JJ==1 : newyyyy=yyyy-1 ; newjjj=365
                else: newyyyy=yyyy ;newjjj=ccfjjj
            elif yyyy!=2017 and jjj==2 :
                if JJ==0 : newyyyy=yyyy-1 ; newjjj=365
                else: newyyyy=yyyy ;newjjj=ccfjjj
            elif yyyy == 2020 and jjj == 366:
                if JJ ==3 : newyyyy=yyyy+1 ; newjjj=1
                elif JJ ==4 : newyyyy=yyyy+1 ; newjjj=2
                else: newyyyy=yyyy ;newjjj=ccfjjj
            elif yyyy == 2020 and jjj == 365:
                if JJ ==4: newyyyy=yyyy+1 ; newjjj=1
                else: newyyyy=yyyy ;newjjj=ccfjjj        
            else: newyyyy=yyyy ;newjjj=ccfjjj
            # print(newyyyy) ;print(newjjj)
        
            ccfpath = CCF_DIR+'/'+pair+'/*'+str(newyyyy)+'.'+strjjj(newjjj)+'*.CCF'
            # print(ccfpath)
            if glob.glob(ccfpath)==[]:
                continue
            else:
                print(ccfpath)    
                st=read(ccfpath)
                CCF=st[0].data
                temp_stk+=CCF
                number+=1
        if number != stkday :
            continue
        else:
            print('----------'+strjjj(jjj)+' Stack'+'-----------')
            CGF=temp_stk/number
            tr=Trace(data=CGF)
            tr.stats.starttime=st[0].stats.starttime
            tr.stats.sampling_rate=40
            tr.stats.station=pair[0:4]
            print('=============')
            CGFfile=CGF_DIR+'/'+pair+'.'+str(yyyy)+'.'+strjjj(jjj)+'.HHZ.CGF'
            print(CGFfile)
            header = st[0].stats.sac
            tr.stats.sac=header
            tr.write(CGFfile,format='SAC')
            print(pair+'DONE')