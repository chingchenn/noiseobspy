# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:46:51 2020

@author: grace
"""


import glob
import pandas as pd
from obspy.core import UTCDateTime

#把txt檔案變成csv檔
pair_list = ['CHS5-CHS4','CHS5-CHS3','CHS5-CHS2','CHS4-CHS2','CHS3-CHS2']
window_list = ['2_6','3_7','4_8','5_9','6_10','7_11','8_12','2_10']
HZ_list = ['1_4','3_6','5_8']
# HZ_list = ['1_4','3_6']
# pair_list = ['CHS4-CHS2']
# window_list = ['5_9']
stakday = 5
for pair in pair_list:
    for window in window_list:
        for HZ in HZ_list:
            CGF_DIR='D:/2020summer/CHS/stretching/02_'+pair+'_CGF5days'
            tempnnn1=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/*'+window+'_'+'n_bp'+HZ+'.txt')[0]
            tempnnn2=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/*'+window+'_'+'n_bp'+HZ+'.txt')[1]
            tempppp1=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/*'+window+'_'+'p_bp'+HZ+'.txt')[0]
            tempppp2=glob.glob('D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/*'+window+'_'+'p_bp'+HZ+'.txt')[1]
            filen1=pd.read_csv(tempnnn1,sep='\s+',header=None,names=['AAA','=','BBB'])
            filen2=pd.read_csv(tempnnn2,sep='\s+',header=None,names=['AAA','=','BBB'])
            filep1=pd.read_csv(tempppp1,sep='\s+',header=None,names=['AAA','=','BBB'])
            filep2=pd.read_csv(tempppp2,sep='\s+',header=None,names=['AAA','=','BBB'])
        
            numbern=pd.concat([filen1.BBB,filen2.BBB])
            numberp=pd.concat([filep1.BBB,filep2.BBB])
            jjjlist=[];sameday=[]
            for ccfpath in sorted(glob.glob(CGF_DIR+'/*.CGF')):
                yyyy=ccfpath.rsplit('.',4)[1]
                if int(yyyy)>2012 and int(yyyy)<2021:
                    julday=ccfpath.rsplit('.',4)[2]
                    jjjlist.append(str(yyyy+'/'+julday))
                    
            dtday = pd.Series(jjjlist)
            for  i , date in enumerate(jjjlist):
                yyyy=date.rsplit('/',2)[0]
                jday=date.rsplit('/',2)[1]
                uuu= UTCDateTime(year=int(yyyy), julday=int(jday))
                sameday.append(uuu)
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
            csvfile=pd.DataFrame({'juliday':jjjlist,'date':sameday,'dvv_n': shiftnlist,
                            'coeff_n': coeffnlist,'dvv_p':shiftplist,'coeff_p':coeffplist})

        
            filename='D:/2020summer/CHS/stretching/count/CGF5days_4s_0.2/'+pair+'/'+pair+'-'+window+'-bp'+HZ+'-nolevel.csv'
            # csvfile.to_csv(filename)
            print(pair+'_'+window+'_bp'+HZ+'_nolevel.csv'+'   DONE')