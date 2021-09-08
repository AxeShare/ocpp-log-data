# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:27:57 2021

@author: Akshay Bhatia
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('jan_log.xlsx')
#df2 = pd.read_excel('nov_log2.xlsx')
#frames = [df1,df2]
#df = pd.concat(frames,axis=0)

bf = df[df.EventName == 'BootNotification']


reboot = []

for i in range(bf.shape[0]):
    #p = af.iloc[i][1]
    cid = bf.iloc[i][1]
    reboot.append(cid)


jf = bf.ReceivedRequest.str.split(",",expand=True)
sf = bf.ServerResponse.str.split(",",expand=True)
frames = [bf,jf,sf]
result = pd.concat(frames,axis=1)
result.to_excel('check.xlsx')

nf = df.drop_duplicates(subset=['EventName'])
loc = []
for index, row in nf.iterrows():
    loc.append(row['EventName'])
    
s1 = 'Unlocked'
s2 = 'NotSupported'
s3 = 'response'
faulty = []
for i in range(bf.shape[0]):
    par = bf.iloc[i][5]
    if s3 in par:
        c = bf.iloc[i][2]
        faulty.append(c)


d = {item:reboot.count(item) for item in reboot}        
r = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

key1 = list(r.keys())
values1 = list(r.values())

chg = list(map(str,key1))
plt.tick_params(axis='x', labelsize=4)
plt.tick_params(axis='y', labelsize=4)
plt.xlabel('ChargerID')
plt.ylabel('Number of reboots')
plt.yticks(np.arange(min(values1), max(values1)+10, 5.0))
plt.bar(chg, values1, width=0.6)
xlocs,xlabs = plt.xticks()
for i, v in enumerate(values1):
    plt.text(xlocs[i] - 0.25, v, str(round(v)),fontsize=3)
plt.xticks(rotation=90)
plt.savefig('reboots.png', dpi=600)
plt.show()

dfr = pd.DataFrame(data=d, index=["Reboots"])
dfr = (dfr.T)

print (df)

dfr.to_excel('reboots_jan.xlsx')
       
        