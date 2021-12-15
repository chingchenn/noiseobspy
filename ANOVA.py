# -*- coding: utf-8 -*-
"""
Created on Tue March 18 22:02:18 2020

@author: Jiching Chen
"""

import csv 
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import leastsq
from mpl_toolkits.mplot3d import Axes3D

file = 'D:/大三學業資料/資料處理/project1/jj2.csv'

data = pd.read_csv(file)
a = data['Column1'].tolist()
b = data['Column2'].tolist()
c = data['Column3'].tolist()
d = data['Column4'].tolist()
e = data['Column5'].tolist()
x = a
y = e
xm = np.mean(x)
ym = np.mean(y)
plt.scatter(x,y,lw = 0.02)

yp_list = []
# new_yp= []
# new_distance = []
# new_copper = []
# yp_list_2 = []
# new_yp_2= []
# new_distance_2 = []
# new_copper_2 = []
# #======================calculate==========================
Xi = np.array(x)
Yi = np.array(y)
def func(p,x):
    k,b = p
    return k*x+b
def error(p,x,y):
    return func(p,x)-y
p0 = [0.3,0.3]
Para = leastsq(error,p0,args=(Xi,Yi))
kX,bX = Para[0]
Para = leastsq(error,p0,args=(Yi,Xi))
kY,bY = Para[0]

X = np.linspace(0,max(x))
Y = kX*X+bX
plt.plot(X,Y,'r')
# plt.ylim(0,2.5)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('y='+str(round(bX,4))+'+'+str(round(kX,4))+'*x')
plt.show()
#========================ANOVA============================
STDx = 0
STDy = 0
cov = 0
for i in range(len(x)):
    yt = kX*x[i]+bX
    xt = kY*y[i]+bY
    yp = (y[i]-yt)
    xp = (x[i]-xt)
    STDx += np.sqrt((y[i]-ym)**2/len(x))
    STDy += np.sqrt((x[i]-xm)**2/len(y))
    cov += (x[i]-xm)**2
    # cov += (x[i]-xm)*(y[i]-ym)/len(x)
    yp_list.append(yp)
# #========================put outlier======================
# for i in range(len(yp_list)):
#      if yp_list[i] > 2*STD:
#         print(i+1,'*======*')
#      else:
#         new_yp.append(yp_list[i])
#         new_distance.append(distance[i])
#         new_copper.append(copper[i])
# Xi_1 = np.array(new_distance)
# Yi_1 = np.array(new_copper)

# Para = leastsq(error,p0,args=(Xi_1,Yi_1))
# k2,b2 = Para[0]
# x = np.linspace(0,new_distance[-1],int(new_distance[-1]*2))
# y = k2*x+b2
# plt.plot(x,y,'r')
# plt.ylim(0,2.5)
# plt.xlabel('distance(m)')
# plt.ylabel('copper(%)')
# plt.plot(new_distance,new_copper,'bo')
# plt.show()        
# #========================ANOVA============================
# STD_2 = 0
# yp_list = []
# for i in range(len(new_distance)):
#     yt = k2*distance[i]+b2
#     yp = (new_copper[i]-yt)**2
#     STD_2 += np.sqrt((new_copper[i]-np.mean(new_copper))**2/len(new_distance))
#     yp_list.append(yp)
# #========================put outlier======================
# for i in range(len(yp_list)):
#      if yp_list[i] > 2*STD_2:
#         print(i+1,'*------*')
#      else:
#         new_yp_2.append(yp_list[i])
#         new_distance_2.append(new_distance[i])
#         new_copper_2.append(new_copper[i])
# Xi_2 = np.array(new_distance_2)
# Yi_2 = np.array(new_copper_2)

# Para = leastsq(error,p0,args=(Xi_2,Yi_2))
# k3,b3 = Para[0]
# x = np.linspace(0,new_distance_2[-1],int(new_distance_2[-1]*2))
# y = k3*x+b3
# plt.plot(x,y,'r')
# # plt.ylim(0,2.5)
# plt.xlabel('distance(m)')
# plt.ylabel('copper(%)')
# plt.plot(new_distance_2,new_copper_2,'bo')
# plt.show()
        
