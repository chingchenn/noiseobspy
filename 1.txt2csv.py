#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:06:50 2020

@author: wtl_st
"""

import glob
import pandas as pd
from obspy.core import UTCDateTime

pair='CHS5-CHS4'
window='3_7'
YEAR='2017-2020'
HZ = '1_4'

CGF_DIR='D:/2020summer/CHS/stretching/02_'+pair+'_CGF5days'
# tempnnn=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_3s_0.2/'+pair+'/*'+YEAR+'_'+window+'_'+'n_bp'+HZ+'.txt')[0]
# tempppp=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_3s_0.2/'+pair+'/*'+YEAR+'_'+window+'_'+'p_bp'+HZ+'.txt')[0]
tempnnn=glob.glob('D:/2020summer/CHS/stretching/count/test/'+pair+'-'+YEAR+'-'+window+'_'+'n_bp'+HZ+'_HHZnew.txt')[0]
tempppp=glob.glob('D:/2020summer/CHS/stretching/count/test/'+pair+'-'+YEAR+'-'+window+'_'+'p_bp'+HZ+'_HHZnew.txt')[0]
filen=pd.read_csv(tempnnn,sep='\s+',header=None,names=['AAA','=','BBB'])
filep=pd.read_csv(tempppp,sep='\s+',header=None,names=['AAA','=','BBB'])
waterpath = 'D:/2020summer/池上/池上地下水.csv'
waterfile=pd.read_csv(glob.glob(waterpath)[0])

length=int(len(filen)/2)
numbern=filen.BBB
numberp=filep.BBB

jjjlist=[]
for ccfpath in sorted(glob.glob(CGF_DIR+'/*.CGF')):
    # print(ccfpath)
    yyyy=ccfpath.rsplit('.',4)[1]
    if int(yyyy)<2017:
        julday=ccfpath.rsplit('.',4)[2]
        jjjlist.append(str(yyyy+'/'+julday))
dtday = pd.Series(jjjlist)
waterday=waterfile.UTC
water=waterfile.level
sameday=[];level=[]
for i , day in enumerate(dtday):
    yyyy=day.rsplit('/',1)[0]
    jjj=day.rsplit('/',1)[1]
    for j , www in enumerate(waterday):
        temp=UTCDateTime(www)
        if int(yyyy)==temp.year and int(jjj)==temp.julday :
            sameday.append(temp)
            level.append(water[j])
            break 
shiftnlist=[]    
for i in range(length):
    III=i*2
    shift=numbern[III]
    # print(shift)
    shiftnlist.append(float(shift))
coeffnlist=[]    
for q in range(length):
    qqq=q*2+1
    coeff=numbern[qqq]
    # print(shift)
    coeffnlist.append(float(coeff))
shiftplist=[]    
for i in range(length):
    III=i*2
    shift=numberp[III]
    # print(shift)
    shiftplist.append(float(-shift))
coeffplist=[]    
for q in range(length):
    qqq=q*2+1
    coeff=numberp[qqq]
    # print(shift)
    coeffplist.append(float(coeff))



csvfile=pd.DataFrame({'juliday':jjjlist,'date':sameday,'waterlevel':level,'dvv_n': shiftnlist,
                      'coeff_n': coeffnlist,'dvv_p':shiftplist,'coeff_p':coeffplist})

filename='D:/2020summer/summer2020/stretching/count/test/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'.csv'
csvfile.to_csv(filename)
print(pair+'_'+YEAR+'_'+window+'_bp'+HZ+'.csv'+'   DONE')