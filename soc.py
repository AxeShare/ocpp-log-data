# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:29:33 2021

@author: Akshay Bhatia
"""

import pandas as pd
import numpy
import matplotlib.pyplot as plt
import statistics
#2,1,10
for1 = [814,815,816,817,818,821,822,826,827,828,829,830,831,839,840,841,843,844,938,1044,1045,1046,1047,1067,1136,1142,1143, 1144]
for2 = [743,753,759,763,767,785,820,824,842,823,765,859,888,889,755,775] #soc 25, tid 27
for3 = [745,771,777,779,789,787,791,833,835,932,1021,1023,1025,1027,1029,1031,1050,1116,1118,1146,1147]
for4 = [761,781,1134] #761 - 47,97   #781 - 47,67
for5 = [783] #tid = 62 #soc 20
for6 = [838,846] #tid = 22 #soc - 20
for7 = [1015,1074,1111] #tid -6  #soc - 22, 1016, 1132, 1139 - data not available
for8 = [1017,1019,1088] #soc - 15
#for10 = [1111] #weirdo #soc - 22 , df = df[pd.notnull(df['20'])]
chgs = for1+for2+for4+for6+for5+for7+for8

soci = []
socf = []

    
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

    
for k in range(len(for8)):
    t = for8[k]
    df = pd.read_excel(f'out_{t}.xlsx')
    df = df[df.EventName == 'MeterValues']
    #df = df[pd.notnull(df['20'])] #for for7
    
    i = 0
    j = 0
    tID = []
    soci_ = []
    socf_ = []
    
    while (i < df.shape[0]):
        try:
            p = df.iloc[i][6]
            p1 = df.iloc[i][36]
            soc = extract_digit(p1)
            #print(soc)
            if soc == 84532:
                soc = 0
            soci_.append(soc)
                
            tID.append(extract_digit(p))
            j = j+1
    
            while(True):
                c1 = df.iloc[i][6]
                t1 = extract_digit(c1)
                if t1 == tID[j-1]:
                    i = i+1
                else:
                    p2 = df.iloc[i-1][36]
                    soc = extract_digit(p2)
                    print(soc)
                    if soc == 84532:
                        soc = 0
                    socf_.append(soc)
                    break
            
            if i > df.shape[0]:
                break
        except IndexError:
            pass
    
    if len(soci_) == 0:
        s1 = 0
    else:
        s1 = statistics.mean(soci_)
    if len(socf_) == 0:
        s2 = 0
    else:
        s2 = statistics.mean(socf_)
    soci.append(s1)
    socf.append(s2)
    print(k)
    
    
N = 56
chg = list(map(str,chgs))
# Data on X-axis

# Specify the values of blue bars (height)
blue_bar = soci
# Specify the values of orange bars (height)
orange_bar = socf

# Position of bars on x-axis
ind = numpy.arange(N)

# Figure size
plt.figure(figsize=(10,5))

# Width of a bar 
width = 0.3       

# Plotting
plt.bar(ind, blue_bar , width, label='Average Initial SoC')
plt.bar(ind + width, orange_bar, width, label='Average Final SoC')

plt.xlabel('ChargerID')
plt.ylabel('State of Charge')
#plt.title('Time Slot Classification')

# xticks()
# First argument - A list of positions at which ticks should be placed
# Second argument -  A list of labels to place at the given locations
plt.tick_params(axis='x', labelsize=4)
plt.xticks(rotation=90)
plt.xticks(ind + width / 2, chg)

# Finding the best position for legends and putting it
plt.legend(loc='best')
plt.savefig('figure1.png',dpi=300)
plt.show()
