# -*- coding: utf-8 -*-
"""
Created on Sat May 22 14:18:41 2021

@author: Akshay Bhatia
"""
import pandas as pd
import numpy as np
import json
import statistics
import matplotlib.pyplot as plt

for1 = [814,815,816,817,818,821,822,826,827,828,829,830,831,839,840,841,843,844,938,1015,1016,1017,1019,1044,1046,1047,1067,1088,1074,1132,1134,1136,1142,1143,1144]
for2 = [743,753,759,763,767,785,820,824,842,823,765,859,888,889,755]
for3 = [745,771,777,779,789,787,791,833,835,932,1021,1045,1023,1025,1027,1029,1031,1050,1116,1118,1146,1147]
for4 = [783] #tid = 62
for5 = [838,846] #tid = 22
for6 = [775,761,781] #weirdos 761-11.3, 781-4.2, 775-16.1
for7 = [1111,1139]

chgs = for1+for2+for3+for4+for6+for5

'''
tot.append(4.2)
avgpt.append(4.2)
ail_.append(0)
til_.append(0)
tID_.append(1)
'''

tot = []    #Energy consumption
avgpt = []

ail_ = []    #Idle loss
til_ = []

tID_ = []

for k in range(len(l3)):
    t = l3[k]
    df = pd.read_excel(f'out_{t}.xlsx')
    df = df[df.EventName == 'MeterValues']
    if t == 1134:
        df = df[:-2]
    i = 0
    j = 0
    tID = []
    expd = []
    start = []
    stop = []

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

    
    while (i < df.shape[0]):
        try:
            p = df.iloc[i][6]
            p1 = df.iloc[i][8]
                
            tID.append(extract_digit(p))
            j = j+1
            ini = extract_digit(p1)
            start.append(ini)
    
            while(True):
                p1 = df.iloc[i][6]
                t1 = extract_digit(p1)
                if t1 == tID[j-1]:
                    i = i+1
                else:
                    p = df.iloc[i-1][8]
                    fin = extract_digit(p)
                    stop.append(fin)
                    break
            val = fin - ini
            expd.append(val/1000)
            if i > df.shape[0]:
                break
        except IndexError:
            pass
           
    if len(expd) == 0:
        m = 0
        s = 0
    else:
        s = sum(expd)
        m = statistics.mean(expd)
    
    if(len(start) and len(stop)):    
        del start[0]
        del stop[-1]
    idleloss = [(a_i - b_i)/1000 for a_i, b_i in zip(start, stop)]
    if len(idleloss) == 0:
        ail = 0
        til = 0
    else:
        til = sum(idleloss)
        ail = statistics.mean(idleloss)
    
    l = len(tID)
    ail_.append(ail)
    til_.append(til)
    avgpt.append(m)
    tot.append(s)
    tID_.append(l)
    print(k)
    '''
    dict1 = dict(zip(sn, common))
    with open('common_charger_ndj.txt', 'w') as file:
        for key, value in dict1.items(): 
            file.write('%s:%s\n' % (key, value))
        file.write(json.dumps(dict1))
     '''       
    
netcons = [a_i + b_i for a_i, b_i in zip(tot, til_)]

dict1 = dict(zip(chgs,tID_)) #non zero transactions
dict2 = dict(zip(chgs,avgpt)) 
dict3 = dict(zip(chgs,tot))
dict4 = dict(zip(chgs,ail_))
dict5 = dict(zip(chgs,til_))
dict6 = dict(zip(chgs,netcons)) 

dicta = dict(zip(norm,til_))
dictb = dict(zip(l3,til1))

r = dict(sorted(dict5.items(), key=lambda item: item[1]))

key1 = list(r.keys())
values1 = list(r.values())

chg = list(map(str,key1))
plt.tick_params(axis='x', labelsize=4)
plt.tick_params(axis='y', labelsize=4)
plt.xlabel('ChargerID')
plt.ylabel('Total Energy Consumption (kWh)')
plt.xticks(rotation=90)
plt.yticks(np.arange(min(values1), max(values1)+10, 500.0))
plt.bar(chg, values1, width=0.8)
xlocs,xlabs = plt.xticks()
for i, v in enumerate(values1):
    plt.text(xlocs[i] - 0.25, v + 0.05, str(round(v)),fontsize=3)
#plt.title('Total Loss')
plt.savefig('8.png', dpi=500)
plt.show()

