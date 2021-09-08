# -*- coding: utf-8 -*-
"""
Created on Sun May 23 23:04:38 2021

@author: Akshay Bhatia
"""


import pandas as pd
import json
import statistics
import matplotlib.pyplot as plt
import re, datetime
import numpy as np


for1 = [814,815,816,817,818,821,822,826,827,828,829,830,831,839,840,841,843,844,938,1015,1016,1017,1019,1044,1046,1047,1067,1074,1088,1111,1132,1134,1136,1139,1142,1143,1144]
for2 = [743,753,759,763,767,785,820,824,842,823,765,755,859,888,889]
#for3 = [745,771,777,779,789,787,791,833,835,932,1021,1023,1025,1027,1045,1029,1031,1050,1116,1118,1146,1147]
for5 = [783] #tid = 62 #ts = 61
for6 = [838,846] #tid = 22 #ts = 21
for4 = [761,775,781] #weirdos  #761 - 8.5 #781 - 0.4 #775 - 1.53

chgs = for1+for2+for4+for5+for6

subfor1 = [831,839,840,841,843,844,938,1017,1019,1044,1046,1047,1067,1088,1132,1134,1136,1142,1143,1144]
subfor2 = [842,859,888,889]
subfor6 = [838]
l3 = [1111,1139]

atu = []
ttu = []

l1 = [783]
l2 = [1015,1016,1074]
outl = l1+l2
'''
atu.append(8.5)
ttu.append(8.5)
atu.append(1.53)
ttu.append(1.53)
atu.append(0.4)
ttu.append(0.4)
'''

def diffmin(p1,p2):
    date1 = re.sub("\D","",p1)
    date2 = re.sub("\D","",p2)
    
    sd1 = []
    sd2 = []
    
    sd1.append(date1[:4])
    sd2.append(date2[:4])
    
    for i in range(4,13,2):
        sd1.append(date1[i:i+2])
        sd2.append(date2[i:i+2])
        
    fd1 = list(map(int,sd1))
    fd2 = list(map(int,sd2))
    a = datetime.datetime(fd1[0], fd1[1], fd1[2], fd1[3], fd1[4], fd1[5])
    b = datetime.datetime(fd2[0], fd2[1], fd2[2], fd2[3], fd2[4], fd2[5])
    c = a-b
    return c.days*24 + c.seconds/3600

def extract_digit(p):
    num1 = ""
    t1 = 0
    for c in p:
        if c.isdigit():
            num1 = num1 + c

    if num1 == "":
        t1 = 84532 #tID[j-1]
    else:
        t1 = int(num1)
    return t1


for k in range(len(l3)):
    t = l3[k]
    df = pd.read_excel(f'out_{t}.xlsx')
    df = df[df.EventName == 'MeterValues']
    if t == 1134:
        df = df[:-2]
    i = 0
    j = 0
    tID = []
    timex = []
           
    while (i < df.shape[0]):
        try:
            p = df.iloc[i][6]
            p1 = df.iloc[i][7]
                
            tID.append(extract_digit(p))
            j = j+1
    
            while(True):
                c1 = df.iloc[i][6]
                t1 = extract_digit(c1)
                if t1 == tID[j-1]:
                    i = i+1
                else:
                    p2 = df.iloc[i-1][7]
                    #p3 = df.iloc[i][7]
                    break
                
            val = diffmin(p2, p1)
            #val1 = diffmin(p3, p2)
            timex.append(val)
            #idt.append(val1)
            if i > df.shape[0]:
                break
        except IndexError:
            pass
           
    if len(timex) == 0:
        m = 0
        s = 0
    else:
        s = sum(timex)
        m = statistics.mean(timex)
            

    atu.append(m)
    ttu.append(s)
    print(k)
    #dict1 = dict(zip(tID, timex))
    #with open(f'time_{t}.txt', 'w') as file:
        #file.write(json.dumps(dict1))

tdt_ = [(744 - b_i)/24 for b_i in ttu]

dict7 = dict(zip(chgs,atu))
dict8 = dict(zip(chgs,ttu)) 
dict9 = dict(zip(chgs,tdt_)) 

dictc = dict(zip(norm,tdt_))
dictd = dict(zip(l3,tdt1))
#dict10 = dict(zip(chgs,total_usage))

r = dict(sorted(dict9.items(), key=lambda item: item[1]))

key1 = list(r.keys())
values1 = list(r.values())

values1[:] = [100*p/744 for p in values1]

chg = list(map(str,key1))
plt.tick_params(axis='x', labelsize=4)
plt.tick_params(axis='y', labelsize=4)
plt.xlabel('ChargerID')
plt.ylabel('Idle Time(%)')
plt.xticks(rotation=90)
plt.yticks(np.arange(0, max(values1)+10, 10.0))
plt.bar(chg, values1, width=0.8)
xlocs,xlabs = plt.xticks()
for i, v in enumerate(values1):
    plt.text(xlocs[i] - 0.25, v + 0.05, str(round(v)),fontsize=3)
#plt.title('Idle Time')
plt.savefig('12.png', dpi=500)
plt.show()


