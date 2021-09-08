# -*- coding: utf-8 -*-
"""
Created on Thu May 13 14:38:59 2021

@author: Akshay Bhatia
"""

#read the data file
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('feb.csv', sep=';')

df1 = pd.read_excel('nov_log1.xlsx')
df2 = pd.read_excel('nov_log2.xlsx')

frames = [df1,df2]
df = pd.concat(frames,axis=0)

#finding total number of chargers and their IDs
uf = df.drop_duplicates(subset=['ChargerID'])
loc = []
for index, row in uf.iterrows():
    loc.append(row['ChargerID'])
loc.sort()
print(loc)


#sort df wrt charger IDs (but quicksort, so timestamp order is not maintained)
b = df.head(10)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(b)

#sort df wrt charger IDs (maintaining correct order of timestamps)
uf = result.loc[result['ChargerID'] == 743]
for i in range(len(loc)):
    t = loc[i]
    dfn = result.loc[result['ChargerID'] == t]
    dfn.to_excel(f'out_{t}.xlsx')
#df1.to_excel('output1.xlsx')    

    
#Extract received request and server response and concatenate with original df    
jf = df.ReceivedRequest.str.split(",",expand=True)
sf = df.ServerResponse.str.split(",",expand=True)
frames1 = [df,jf,sf]
result = pd.concat(frames1,axis=1)

result = result[result.EventName != 'StatusNotification']

result.columns = result.columns.astype(str)
del result['1_2']

#deal with columns with same name
cols = []
count = 1
for column in result.columns:
    if column == '6':
        cols.append(f'6_{count}')
        count+=1
        continue
    cols.append(column)
result.columns = cols

result.to_excel('seg_output.xlsx')

'''
#df["col1"].replace(di, inplace=True) - replace with dictionary values
dur = []
cons = []
rev = []
nt = []
#segregate separate file for each charger
for j in loc:
    df1 = rf.loc[rf['Charger Code'] == j]
    d = []
    c = []
    r = []
    for i in range(df1.shape[0]):
        d.append(df1.iloc[i][13])
        c.append(df1.iloc[i][14])
        r.append(df1.iloc[i][16])
    dur.append(sum(d))
    cons.append(sum(c))
    rev.append(sum(r))
    nt.append(df1.shape[0])
    
dictd = dict(zip(loc,durh))
dictw = dict(zip(loc,cons))
dictr = dict(zip(loc,rev))
dictt = dict(zip(loc,nt))

r = dict(sorted(dictt.items(), key=lambda item: item[1]))

key1 = list(r.keys())
values1 = list(r.values())


chg = list(map(str,key1))
plt.tick_params(axis='x', labelsize=4)
plt.tick_params(axis='y', labelsize=4)
plt.xlabel('ChargerID')
plt.ylabel('No. of transactions')
plt.xticks(rotation=90)
plt.yticks(np.arange(min(values1), max(values1)+10, 20.0))
plt.bar(chg, values1, width=0.8)
xlocs,xlabs = plt.xticks()
#for i, v in enumerate(values1):
    #plt.text(xlocs[i] - 0.25, v + 0.05, str(v),fontsize=3)
plt.savefig('transactions.png', dpi=300)
plt.show()
'''  