# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:18:06 2020

@author: grace
"""

import os
import glob
import pandas as pd
from obspy.core import UTCDateTime

#把txt檔案變成csv檔並且加上了地下水位高度
# YEAR='2013-2016'
# pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
window_list = ['2_6','3_7','4_8','5_9','6_10','7_11','8_12','2_10']
# window_list = ['2_5','3_6','4_7','5_8','6_9','7_10','8_11','2_10']
# HZ_list = ['1_4','3_6','5_8']
HZ_list = ['1_4']
pair_list = ['CHS4-CHS2']
window_list = ['2_6']
stakday = 5
for pair in pair_list:
    for window in window_list:
        for HZ in HZ_list:
            CGF_DIR='D:/2020summer/CHS/stretching/02_'+pair+'_CGF5days'
            tempnnn1=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/2_8hz2013.new.txt')[0]
            tempnnn2=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/2_8hz.new.txt')[0]
            tempppp1=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/2_8hz2013.newp.txt')[0]
            tempppp2=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/2_8hz.newp.txt')[0]
            filen1=pd.read_csv(tempnnn1,sep='\s+',header=None,names=['AAA','=','BBB'])
            filen2=pd.read_csv(tempnnn2,sep='\s+',header=None,names=['AAA','=','BBB'])
            filep1=pd.read_csv(tempppp1,sep='\s+',header=None,names=['AAA','=','BBB'])
            filep2=pd.read_csv(tempppp2,sep='\s+',header=None,names=['AAA','=','BBB'])
            waterpath = 'D:/2020summer/池上/池上地下水.csv'
            waterfile=pd.read_csv(glob.glob(waterpath)[0])
        
            numbern=pd.concat([filen1.BBB])
            numberp=pd.concat([filep1.BBB,filep2.BBB])
            jjjlist=[]
            for ccfpath in sorted(glob.glob(CGF_DIR+'/*.CGF')):
                yyyy=ccfpath.rsplit('.',4)[1]
                if int(yyyy)>2012 and int(yyyy)<2020:
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
                else:print(yyyy,jjj)
            shiftnlist=[]    
            for i in range(len(jjjlist)):
                III=i*2
                shift=numbern[III]
                shiftnlist.append(float(shift))
            coeffnlist=[]    
            for q in range(len(jjjlist)):
                qqq=q*2+1
                coeff=numbern[qqq]
                coeffnlist.append(float(coeff)) 
            shiftplist=[]    
            for i in range(len(jjjlist)):
                III=i*2
                shift=numberp[III]
                shiftplist.append(float(-shift))
            coeffplist=[]    
            for q in range(len(jjjlist)):
                qqq=q*2+1
                coeff=numberp[qqq]
                coeffplist.append(float(coeff))
            csvfile=pd.DataFrame({'juliday':jjjlist,'date':sameday,'waterlevel':level,'dvv_n': shiftnlist,
                            'coeff_n': coeffnlist,'dvv_p':shiftplist,'coeff_p':coeffplist})
            # csvfile=pd.DataFrame({'juliday':jjjlist,'date':sameday,'waterlevel':level,'dvv_n': shiftnlist,
                            # 'coeff_n': coeffnlist})

        
            filename='D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/NNN.csv'
            csvfile.to_csv(filename)
            print(pair+'_'+window+'_bp'+HZ+'.csv'+'   DONE')