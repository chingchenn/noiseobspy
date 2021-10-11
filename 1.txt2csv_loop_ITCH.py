# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 22:42:27 2020

@author: grace
"""

import glob
import pandas as pd
from obspy.core import UTCDateTime

YEAR='2013-2016'
pair_list = ['IT01-IT03','IT01-IT04','IT01-IT05','IT01-IT07','IT01-IT09','IT02-IT01','IT02-IT03','IT02-IT04','IT02-IT05','IT02-IT06','IT02-IT07','IT02-IT08','IT02-IT09','IT02-IT10',
              'IT03-IT04','IT03-IT05','IT03-IT07','IT03-IT09','IT04-IT05','IT04-IT07','IT06-IT01','IT06-IT01','IT06-IT03','IT06-IT05','IT06-IT07','IT06-IT08','IT06-IT09','IT06-IT10',
              'IT07-IT05','IT08-IT01','IT08-IT03','IT08-IT04','IT08-IT05','IT08-IT07','IT09-IT05','IT09-IT04','IT10-IT01','IT10-IT03','IT10-IT04','IT10-IT05','IT10-IT07','IT10-IT09']
window_list = ['2_10','2_3','2_6']
HZ_list = ['3_5','2_4','0.5_1','0.1_0.5']
for pair in pair_list:
    for window in window_list:
        for HZ in HZ_list:
            CGF_DIR='D:/2020summer/ITCH/stretching/'+pair+'_CGF5days'
            tempnnn=glob.glob('D:/2020summer/ITCH/stretching/count/'+pair+'/*'+window+'_'+'n_bp'+HZ+'.txt')[0]
            tempppp=glob.glob('D:/2020summer/ITCH/stretching/count/'+pair+'/*'+window+'_'+'p_bp'+HZ+'.txt')[0]
            filen=pd.read_csv(tempnnn,sep='\s+',header=None,names=['AAA','=','BBB'])
            filep=pd.read_csv(tempppp,sep='\s+',header=None,names=['AAA','=','BBB'])
            # waterpath = 'D:/2020summer/池上/Chihshang_groundwater_level_2013-2016.csv'
            # waterfile=pd.read_csv(glob.glob(waterpath)[0])
            length=int(len(filen)/2)
        
            numbern=filen.BBB
            numberp=filep.BBB
            jjjlist=[]
            for ccfpath in sorted(glob.glob(CGF_DIR+'/*.CGF')):
                yyyy=ccfpath.rsplit('.',4)[1]
                if int(yyyy)<2017:
                    julday=ccfpath.rsplit('.',4)[2]
                    jjjlist.append(str(yyyy+'/'+julday))
            dtday = pd.Series(jjjlist)
            # waterday=waterfile.UTC
            # water=waterfile.level
            sameday=[];level=[]
            for i , day in enumerate(dtday):
                yyyy=day.rsplit('/',1)[0]
                jjj=day.rsplit('/',1)[1]
                sameday.append(yyyy+'/'+jjj)
                # for j , www in enumerate(waterday):
                    # temp=UTCDateTime(www)
                    # if int(yyyy)==temp.year and int(jjj)==temp.julday :
                        # sameday.append(temp)
                        # level.append(water[j])
                        # break 
            shiftnlist=[]    
            for i in range(length):
                III=i*2
                shift=numbern[III]
                shiftnlist.append(float(shift))
            coeffnlist=[]    
            for q in range(length):
                qqq=q*2+1
                coeff=numbern[qqq]
                coeffnlist.append(float(coeff))
            shiftplist=[]    
            for i in range(length):
                III=i*2
                shift=numberp[III]
                shiftplist.append(float(shift))
            coeffplist=[]    
            for q in range(length):
                qqq=q*2+1
                coeff=numberp[qqq]
                coeffplist.append(float(coeff))
            # csvfile=pd.DataFrame({'juliday':jjjlist,
            #                   'date':sameday,
            #                 'waterlevel':level,
            #                 'dvv_n': shiftnlist,
            #                 'coeff_n': coeffnlist,
            #                 'dvv_p':shiftplist,
            #                 'coeff_p':coeffplist})
            csvfile=pd.DataFrame({'juliday':jjjlist,
                              # 'date':sameday,
                            'dvv_n': shiftnlist,
                            'coeff_n': coeffnlist,
                            'dvv_p':shiftplist,
                            'coeff_p':coeffplist})
        
            filename='D:/2020summer/ITCH/stretching/count/'+pair+'/'+pair+'_'+YEAR+'_'+window+'_bp'+HZ+'.csv'
            csvfile.to_csv(filename)
            print(pair+'_'+YEAR+'_'+window+'_bp'+HZ+'.csv'+'   DONE')