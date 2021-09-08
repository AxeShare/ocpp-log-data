
import re
import pandas as pd
from datetime import datetime
from dateutil import tz
import numpy
import matplotlib.pyplot as plt
import collections

for1 = [814,815,816,817,818,821,822,826,827,828,829,830,831,839,840,841,843,844,938,1015,1016,1017,1019,1044,1046,1047,1067,1074,1088,1111,1132,1134,1136,1139,1142,1143,1144]
for2 = [743,753,759,763,767,785,820,824,842,823,765,755,859,888,889,775]
#for3 = [745,771,777,779,789,787,791,833,835,932,1021,1023,1025,1027,1045,1029,1031,1050,1116,1118,1146,1147]
for5 = [783] #tid = 62
for6 = [838,846] #tid = 22
for4 = [761,781]
chgs = for1+for2+for4+for6+for5

mp = []
ap = []
ep = []
np = []

'''
for4
mp.append(0)
ap.append(0)
ep.append(100)
np.append(0)
'''

def find_slot(s):
    d1 = re.sub("\D","",s)
    
    dat1 = []
    dat1 = d1[:4]+'-'+d1[4:6]+'-'+d1[6:8]+' '+d1[8:10]+':'+d1[10:12]+':'+d1[12:14]
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    utc = datetime.strptime(dat1, '%Y-%m-%d %H:%M:%S') #'2020-12-01 09:02:39'
    utc = utc.replace(tzinfo=from_zone)
    
    central = utc.astimezone(to_zone)
    h = central.hour
    if(h>=3 and h<=9):
        return 'morning'
    elif(h>9 and h<=15):
        return 'afternoon'
    elif(h>15 and h<=21):
        return 'evening'
    elif(h>21 or h<3):
        return 'night'
    
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
    t_m = 0
    t_a = 0
    t_e = 0
    t_n = 0
           
    while (i < df.shape[0]):
        try:
            p = df.iloc[i][62]
            p1 = df.iloc[i][61]
            slot = find_slot(p1)
                
            tID.append(extract_digit(p))
            j = j+1
    
            while(True):
                c1 = df.iloc[i][62]
                t1 = extract_digit(c1)
                if t1 == tID[j-1]:
                    i = i+1
                else:
                    #p2 = df.iloc[i][7]
                    #slot = find_slot(p2)
                    break
            if slot == 'morning':
                t_m += 1
            elif slot == 'afternoon':
                t_a += 1
            elif slot == 'evening':
                t_e += 1
            elif slot == 'night':
                t_n += 1
            
            if i > df.shape[0]:
                break
        except IndexError:
            pass
    tt = t_m + t_a + t_e + t_n
    mp.append(100*t_m/tt)
    ap.append(100*t_a/tt)
    ep.append(100*t_e/tt)
    np.append(100*t_n/tt)
      
    print(t_m,t_a,t_e,t_n,k)


dictm = dict(zip(chgs,mp))
dicta = dict(zip(chgs,ap)) 
dicte = dict(zip(chgs,ep))
dictn = dict(zip(chgs,np))

od1 = collections.OrderedDict(sorted(dictm.items()))
od2 = collections.OrderedDict(sorted(dicta.items()))
od3 = collections.OrderedDict(sorted(dicte.items()))
od4 = collections.OrderedDict(sorted(dictn.items()))

x = []
mp1 = []
ap1 = []
ep1 = []
np1 = []


for k, v in od1.items():
    x.append(k)
    mp1.append(v)
    
for k, v in od2.items():
    ap1.append(v)

for k, v in od3.items():
    ep1.append(v)
    
for k, v in od4.items():
    np1.append(v)

xf = x[:29]
xs = x[29:]
mpf = mp1[:29]
mps = mp1[29:]
apf = ap1[:29]
aps = ap1[29:]
epf = ep1[:29]
eps = ep1[29:]
npf = np1[:29]
nps = np1[29:]

N =29
ind = numpy.arange(N)
width = 0.6
chg = list(map(str,xs))
# Data on X-axis

mp2 = numpy.array(mps)
ap2 = numpy.array(aps)
ep2 = numpy.array(eps)
np2 = numpy.array(nps)

plt.figure(figsize=(10,5))
p1 = plt.bar(ind, mp2, width, color='r')
p2 = plt.bar(ind, ap2, width, bottom=mp2, color='b')
p3 = plt.bar(ind, ep2, width, bottom=mp2+ap2, color='g')
p3 = plt.bar(ind, np2, width, bottom=mp2+ap2+ep2, color='c')
#p4 = plt.bar([i for i in ind], y2, width=0.7, color='y', alpha=0.5, label='Number of transactions(x5)')

plt.xlabel('ChargerID')
plt.ylabel('Usage Slot percentage')
#plt.title('Time Slot Classification')

# xticks()
# First argument - A list of positions at which ticks should be placed
# Second argument -  A list of labels to place at the given locations
plt.tick_params(axis='x', labelsize=6)
plt.xticks(rotation=90)
plt.xticks(ind, chg)

# Finding the best position for legends and putting it
#plt.legend(loc = 'best')
plt.ylim([0,110])
plt.savefig('3.png',dpi=500)
plt.show()

'''
# Specify the values of blue bars (height)
blue_bar = mp
# Specify the values of orange bars (height)
orange_bar = ap
green_bar = ep
red_bar = np

# Position of bars on x-axis
#ind = numpy.arange(N)

# Figure size
plt.figure(figsize=(10,5))

# Width of a bar 
width = 0.2       

# Plotting
plt.bar(ind, blue_bar , width, label='12AM - 6AM')
plt.bar(ind + width, orange_bar, width, label='6AM - 12PM')
plt.bar(ind + 2*width, green_bar, width, label = '12PM - 6PM')
plt.bar(ind + 3*width, red_bar, width, label = '6PM - 12AM')

plt.xlabel('ChargerID')
plt.ylabel('Usage Slot percentage')
plt.title('Time Slot Classification')

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
'''