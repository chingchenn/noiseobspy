#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:50:56 2020

@author: wtl_st
"""


import numpy as np
import datetime as dt
from scipy import stats
import matplotlib as mpl
import sys, obspy, os,glob
import matplotlib.pyplot as plt
from obspy.io.sac import SACTrace
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
from obspy import read, read_inventory,Trace

sys.setrecursionlimit(100000)
date1 = dt.datetime(2017, 1, 1)
date2 = dt.datetime(2021, 1, 1)
delta= dt.timedelta(days=1)
dates= mpl.dates.drange(date1, date2, delta)

CCF_DIR='D:/2020summer/CHS/D03_CCF'
stkday=11
pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
pair_list = ['CHS5-CHS3']
for pair in pair_list:
    CGF_DIR='D:/2020summer/CHS/stretching/'+pair+'_CGF11days'
    if not os.path.isdir(CGF_DIR):
        os.makedirs(os.path.join(CGF_DIR))
    def strjjj(jjj):
        jjj=str(jjj)
        if len(jjj)==1:
            return '00'+jjj
        elif len(jjj)==2:
            return '0'+jjj
        else: return jjj
    def stk5days(yyyy,jjj):
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
        return newyyyy,newjjj
    
        
        
    def stk11days(yyyy,jjj):
        global newyyyy ;global newjjj
        if yyyy != 2020 and jjj == 361 :
            if JJ==10 : newyyyy=yyyy+1 ;  newjjj=1
            else: newyyyy=yyyy ;newjjj=ccfjjj
        elif yyyy != 2020 and jjj == 362 :
            if JJ==9 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>9 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj    
        elif yyyy != 2020 and jjj == 363 :
            if JJ==8 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>8 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj  
        elif yyyy != 2020 and jjj == 364 :
            if JJ==7 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>7 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy != 2020 and jjj == 365 :
            if JJ==6 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>6 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 362:
            if JJ==10 : newyyyy=yyyy+1 ;  newjjj=1
            else: newyyyy=yyyy ;newjjj=ccfjjj
        elif yyyy == 2020 and jjj == 363 :
            if JJ==9 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>9 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 364 :
            if JJ==8 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>8 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 365 :
            if JJ==7: newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>7 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 366 :
            if JJ==6 : newyyyy=yyyy+1 ;  newjjj=1
            elif JJ>6 : newyyyy=newyyyy;newjjj+=1  
            else: newyyyy=yyyy ;newjjj=ccfjjj
    ###==================================================
        elif yyyy != 2020 and jjj == 1 :
            if JJ==0: newyyyy=yyyy-1;newjjj=361
            elif 0<JJ<5:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy != 2020 and jjj == 2 :
            if JJ==0: newyyyy=yyyy-1;newjjj=362
            elif 0<JJ<4:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj    
        elif yyyy != 2020 and jjj == 3 :
            if JJ==0: newyyyy=yyyy-1;newjjj=363
            elif 0<JJ<3:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj
        elif yyyy != 2020 and jjj == 4 :
            if JJ==0: newyyyy=yyyy-1;newjjj=364
            elif 0<JJ<2:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj
        elif yyyy != 2020 and jjj == 5 :
            if JJ==0: newyyyy=yyyy-1;newjjj=365
            else: newyyyy=yyyy ;newjjj=ccfjjj
        elif yyyy == 2020 and jjj == 1 :
            if JJ==0: newyyyy=yyyy-1;newjjj=362
            elif 0<JJ<5:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj   
        elif yyyy == 2020 and jjj == 2 :
            if JJ==0: newyyyy=yyyy-1;newjjj=363
            elif 0<JJ<4:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 3 :
            if JJ==0: newyyyy=yyyy-1;newjjj=364
            elif 0<JJ<3:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 4 :
            if JJ==0: newyyyy=yyyy-1;newjjj=365
            elif 0<JJ<2:newyyyy=newyyyy;newjjj+=1 
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        elif yyyy == 2020 and jjj == 5 :
            if JJ==0: newyyyy=yyyy-1;newjjj=366
            else: newyyyy=yyyy ;newjjj=ccfjjj 
        else: newyyyy=yyyy ;newjjj=ccfjjj
        
        
        return newyyyy,newjjj    
    
    
        
    for UTC in dates:
        UUU=UTCDateTime(mpl.dates.num2date(UTC))
        
        jjj=UUU.julday
        print(jjj)
        print('=================================')
        temp_stk=0;number=0
        for JJ in range(stkday):
            yyyy=UUU.year
            ccfjjj=jjj+JJ-5     ##-----------------------------------have to adjust
            
            newyyyy,newjjj=stk11days(yyyy,jjj)
            
            # print(newyyyy) ;print(newjjj)
        
            ccfpath = CCF_DIR+'/'+pair+'/*'+str(newyyyy)+'.'+strjjj(newjjj)+'*.CCF'
            # print(ccfpath)
            if glob.glob(ccfpath)==[]:
                continue
            else:
                # print(ccfpath)    
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