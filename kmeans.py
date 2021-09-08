# -*- coding: utf-8 -*-
"""
Created on Wed May 26 21:53:49 2021

@author: Akshay Bhatia
"""
import re
import pandas as pd
from datetime import datetime
from dateutil import tz
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

for1 = [814,815,816,817,818,821,822,826,827,828,829,830,831,839,840,841,843,844,938,1015,1016,1017,1019,1044,1045,1046,1047,1067,1074,1088,1111,1132,1134,1136,1139,1142,1143,1144]
for2 = [743,753,759,763,767,785,820,824,842,823,765,755,859,888,889,775,761,781]
for3 = [745,771,777,779,789,787,791,833,835,932,1021,1023,1025,1027,1029,1031,1050,1116,1118,1146,1147]
for4 = [783] #tid = 62
for5 = [838,846] #tid = 22  #0.1,8.5   #2.28,2.683
chgs = for1+for2+for4+for6+for5

arr_ = []
dep_ = []

def find_slot(s):
    d1 = re.sub("\D","",s)
    
    dat1 = []
    dat1 = d1[:4]+'-'+d1[4:6]+'-'+d1[6:8]+' '+d1[8:10]+':'+d1[10:12]+':'+d1[12:14]
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    utc = datetime.strptime(dat1, '%Y-%m-%d %H:%M:%S') #'2020-12-01 09:02:39'
    utc = utc.replace(tzinfo=from_zone)
    
    central = utc.astimezone(to_zone)
    h = central.hour + central.minute/60 + central.second/3600
    return h
    
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

    
for k in range(len(for5)):
    t = for5[k]
    df = pd.read_excel(f'out_{t}.xlsx')
    df = df[df.EventName == 'MeterValues']
    if t == 1134:
        df = df[:-2]
    i = 0
    j = 0
    tID = []
           
    while (i < df.shape[0]):
        try:
            p = df.iloc[i][22]
            p1 = df.iloc[i][21]
            arr = find_slot(p1)
            arr_.append(arr)
                
            tID.append(extract_digit(p))
            j = j+1
    
            while(True):
                c1 = df.iloc[i][22]
                t1 = extract_digit(c1)
                if t1 == tID[j-1]:
                    i = i+1
                else:
                    p2 = df.iloc[i-1][21]
                    dep = find_slot(p2)
                    dep_.append(dep)
                    break
            
            if i > df.shape[0]:
                break
        except IndexError:
            pass
    print(k)

df1 = pd.DataFrame({'Arrival': arr_,'Departure':dep_,})

kmeans = KMeans(n_clusters=4, random_state=0, algorithm="elkan")
df1['cluster'] = kmeans.fit_predict(df1[['Arrival', 'Departure']])
# get centroids
centroids = kmeans.cluster_centers_
cen_x = [i[0] for i in centroids] 
cen_y = [i[1] for i in centroids]
## add to df
df1['cen_x'] = df1.cluster.map({0:cen_x[0], 1:cen_x[1], 2:cen_x[2], 3:cen_x[3]})
df1['cen_y'] = df1.cluster.map({0:cen_y[0], 1:cen_y[1], 2:cen_y[2], 3:cen_y[3]})
# define and map colors
colors = ['red', 'green', 'blue', 'yellow']
df1['c'] = df1.cluster.map({0:colors[0], 1:colors[1], 2:colors[2], 3:colors[3]})
plt.xlabel('Time of arrival (hh:mm)')
plt.ylabel('Time of departure (hh:mm)')
plt.xticks(numpy.arange(0,24.0,6.0))
plt.yticks(numpy.arange(0,24.0,6.0))
plt.scatter(df1.Arrival, df1.Departure, c=df1.c, alpha = 0.6, s=2)
plt.savefig('figure2.png',dpi=300)
plt.show()

diff = []
c = []
for i in range(df1.shape[0]):
    h = df1.Departure[i] - df1.Arrival[i]
    if h<0:
        h = h + 24
    diff.append(h)
    if(h>=0 and h<=6):
        c.append('r')
    elif(h>6 and h<=12):
        c.append('g')
    elif(h>12 and h<=18):
        c.append('b')
    elif(h>18 and h<=24):
        c.append('y')

plt.xlabel('Time of arrival (hh:mm)')
plt.ylabel('Time of departure (hh:mm)')
plt.xticks(numpy.arange(0,30,6.0))
plt.yticks(numpy.arange(0,30,6.0))
plt.scatter(df1.Arrival, df1.Departure, marker='x' ,c=df1.col, alpha = 0.6, s=2)
#plt.legend(['ctime < 6h', 'ctime < 12h', 'ctime < 18h', 'ctime > 24h'],fontsize=8)
#plt.legend(['ctime < 12h', 'ctime < 18h', 'ctime > 24h'],fontsize=6)
plt.savefig('figure2.png',dpi=300)
plt.show()

group = df1.col
cdict = {'r': 'ctime < 6h', 'g': 'ctime < 12h', 'b': 'ctime < 18h', 'y': 'ctime > 18h'}

'''
fig, ax = plt.subplots()
for g in numpy.unique(group):
    ix = numpy.where(group == g)
    ax.scatter(df1.Arrival[ix], df1.Departure[ix], c = cdict[g], label = g, s = 2)
ax.legend()
plt.show()

plt.legend(p,
           ('Low Outlier', 'LoLo', 'Lo', 'Average', 'Hi', 'HiHi', 'High Outlier'),
           scatterpoints=1,
           loc='lower left',
           ncol=3,
           fontsize=8)
'''
X = []

for i in range(df1.shape[0]):
    l = []
    for j in range(2):
        l.append(df1.iloc[i][j])
    X.append(l)
    
Y = np.array([np.array(xi) for xi in X])

clustering = DBSCAN(eps=1, min_samples=90).fit(Y)

df1['DBSCAN_opt_labels']= clustering.labels_

print(df1['DBSCAN_opt_labels'].value_counts())

L = list(clustering.labels_)
c = []
for j in L:
    if(not j):
        c.append('r')
    elif(not j+1):
        c.append('g')
    elif(j==2):
        c.append('b')
    elif(j==-1):
        c.append('y')
    elif(j==3):
        c.append('c')

df1['coldb'] = c

plt.xlabel('Time of arrival (hh:mm)')
plt.ylabel('Time of departure (hh:mm)')
plt.xticks(np.arange(0,30,6.0))
plt.yticks(np.arange(0,30,6.0))
plt.scatter(df1.Arrival, df1.Departure, marker='o' ,c=df1.coldb, alpha = 0.6, s=2)
plt.savefig('figuredb1.png',dpi=300)
plt.show()

