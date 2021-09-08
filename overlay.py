# -*- coding: utf-8 -*-
"""
Created on Thu May 27 15:50:33 2021

@author: Akshay Bhatia
"""


import matplotlib.pyplot as plt
import numpy as np
import collections

dict3 = {}
dict1 = {}

od1 = collections.OrderedDict(sorted(dictb.items()))
od2 = collections.OrderedDict(sorted(dictd.items()))

x = []
y1 = []
y2 = []


for k, v in od1.items():
    x.append(k)
    y1.append(v)
    

for k, v in od2.items():
    y2.append(v)
 
'''
xf = x[:27]
xs = x[27:]
y1f = y1[:27]
y1s = y1[27:]
y2f = y2[:27]
y2s = y2[27:]


for t in y2:
    if t > 300:
        y2s.append(t)
        idx = y2.index(t)
        xs.append(x[idx])
        y1s.append(y1[idx])
        del y2[idx]
        del x[idx]
        del y1[idx]
'''

x1 = list(map(str,x))

#y2f[:] = [p/24 for p in y2f]

width = 0.2
indices = np.arange(len(y1))

plt.bar(indices, y1, width=width, 
        color='b')
plt.bar([i for i in indices], y2, 
        width=0.6*width, color='r', alpha=0.5)

plt.xticks(indices, [x1[i] for i in range(len(y1))])
           #['T{}'.format(i) for i in range(len(y1))] )
plt.tick_params(axis='x', labelsize=5)
plt.tick_params(axis='y', labelsize=5)
#plt.xticks(rotation=90)
plt.xlabel('ChargerID')
plt.legend()
plt.yticks(np.arange(-100, 30, 10.0))
xlocs,xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i], v + 0.05, str(round(v,2)),fontsize=5)
for i, v in enumerate(y2):
    plt.text(xlocs[i], v + 0.05, str(round(v,2)),fontsize=5)
#plt.title('Total Loss vs Idle Time')
plt.savefig('loss-idle-m2.png', dpi=500)
plt.show()






x1 = list(map(str,xs))

y2s[:] = [p/24 for p in y2s]

width = 0.6
indices = np.arange(len(y1s))

plt.bar(indices, y1s, width=width, 
        color='b')
plt.bar([i for i in indices], y2s, 
        width=0.6*width, color='r', alpha=0.5)

plt.xticks(indices, [x1[i] for i in range(len(y1s))])
           #['T{}'.format(i) for i in range(len(y1))] )
plt.tick_params(axis='x', labelsize=5)
plt.tick_params(axis='y', labelsize=5)
#plt.xticks(rotation=90)
plt.xlabel('ChargerID')
plt.legend()
plt.yticks(np.arange(0, 3800, 200.0))
xlocs,xlabs = plt.xticks()
for i, v in enumerate(y1s):
    plt.text(xlocs[i] - 0.25, v + 0.05, str(round(v,2)),fontsize=3)
for i, v in enumerate(y2s):
    plt.text(xlocs[i] - 0.25, v + 0.05, str(round(v,2)),fontsize=3)
#plt.title('Total Loss vs Idle Time')
plt.savefig('loss-idle2.png', dpi=500)
plt.show()

