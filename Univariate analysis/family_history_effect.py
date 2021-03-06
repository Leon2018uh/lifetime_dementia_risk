import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import set_option
import os

set_option('display.width', 2000)
pd.set_option("display.max_rows", 500, "display.max_columns", 2000)
set_option('precision', 3)
#set_option("display.max_rows", 10)
pd.options.mode.chained_assignment = None

input_file = './raw data_edit/data_merge.csv'    # The well name of an input file
data_input_ori = pd.read_csv(input_file)
j=0
for i in range(data_input_ori.shape[0]):
    sumbox_clc = data_input_ori.commun[i] + data_input_ori.homehobb[i] + data_input_ori.judgment[i] + \
        data_input_ori.memory[i] + data_input_ori.orient[i] + data_input_ori.perscare[i]
    if sumbox_clc != data_input_ori.sumbox[i]:
        #print(sumbox_clc, data_input_ori.sumbox[i])
        data_input_ori.sumbox[i] = sumbox_clc
        j = j+1
print(j)

#data_input = data_input_ori[(data_input_ori.cdr < 1.0) | (data_input_ori.sumbox > 2.0)]
data_input = data_input_ori

M, N = data_input.shape
print(M, N)
keys = data_input.keys()
print(keys)

# Calculate clinic dementia rating for label
data_diag = data_input[['cdr', 'sumbox', 'mmse', 'commun', 'homehobb', 'judgment', 'memory', 'orient', 'perscare']]
feature = data_input[['mmse', 'commun', 'homehobb', 'judgment', 'memory', 'orient', 'perscare']]
label = data_input['sumbox']

feature_st = data_diag.describe()
#print(feature_st)
# Plot the results
font = {'family': 'normal', 'size': 18}
plt.rc('font', **font)

#data_diag.hist(grid=False, bins=6)

plt.figure(2)
plt.scatter(data_input.cdr, data_input.sumbox)
plt.xlabel('CDR')
plt.ylabel('sumbox')

plt.figure(3)
plt.scatter(data_input_ori.cdr, data_input_ori.sumbox)
plt.xlabel('CDR')
plt.ylabel('sumbox')


x1 = len(data_diag[(data_diag.sumbox<0.5)]) / M
x2 = len(data_diag[(data_diag.sumbox>=0.5) & (data_diag.sumbox < 5.0) ]) / M
x3 = len(data_diag[(data_diag.sumbox>=5.0) & (data_diag.sumbox < 10.0) ]) / M
x4 = len(data_diag[(data_diag.sumbox>=10.0) & (data_diag.sumbox < 15.0) ]) / M
x5 = len(data_diag[(data_diag.sumbox>=15.0) & (data_diag.sumbox < 35.0) ]) / M
print(x1)
data_pie = [x1, x2, x3, x4, x5]
explode = (0.1, 0.0, 0, 0, 0.0)
labels = ['Normal', 'Mild impairment', '', '', 'Dementia']
f, bx = plt.subplots(nrows=1, ncols=1)
#autopct='%1.1f%%'
bx.pie(data_pie, explode=explode, labels=labels, shadow=True, startangle=90)
#bx.hist(attr1, bins=22, density=True, color='r', histtype='bar', label='CDR < 0.5')
#bx.legend()
#bx.set_ylim(ztop, zbot)
#bx.invert_yaxis()
#bx.grid()
#bx.locator_params(axis='x', nbins=7)
#bx.set_xlabel("sumbox")
#bx.set_ylabel("Probability density (%)")
#bx.set_xlim(np.min(Udry) - 3, np.max(Udry) + 5)


# Create date for prediciton model
data_fd = data_input[['Subject', 'sumbox', 'Age', 'apoe', 'M/F', 'Hand', 'Education', 'Race', 'LIVSIT', 'INDEPEND', 'RESIDENC', 'MARISTAT', 'BMI', 'dem_idx', 'CVHATT', 'CVAFIB', 'CVANGIO', 'CVBYPASS', 'CVPACE', 'CVCHF', 'CVOTHR', 'CBSTROKE', 'CBTIA', 'CBOTHR', 'PD', 'PDOTHR', 'SEIZURES', 'TRAUMBRF', 'TRAUMEXT', 'TRAUMCHR', 'NCOTHR', 'HYPERTEN', 'HYPERCHO', 'DIABETES', 'B12DEF', 'THYROID', 'INCONTU', 'INCONTF', 'DEP2YRS', 'DEPOTHR', 'ALCOHOL', 'TOBAC30', 'TOBAC100', 'SMOKYRS', 'PACKSPER', 'ABUSOTHR', 'PSYCDIS', 'GDS']]
data_fd1 = data_input[['Age', 'apoe', 'M/F', 'Hand', 'Education', 'Race', 'LIVSIT', 'INDEPEND', 'RESIDENC']]
data_fd2 = data_input[['MARISTAT', 'BMI', 'dem_idx', 'CVHATT', 'CVAFIB', 'CVANGIO', 'CVBYPASS', 'CVPACE', 'CVCHF']]
data_fd3 = data_input[['CBSTROKE', 'CBTIA', 'CBOTHR', 'PD', 'PDOTHR', 'SEIZURES', 'TRAUMBRF', 'TRAUMEXT', 'TRAUMCHR']]
data_fd4 = data_input[['HYPERTEN', 'HYPERCHO', 'DIABETES', 'B12DEF', 'THYROID', 'INCONTU', 'INCONTF', 'DEP2YRS', 'DEPOTHR']]
data_fd5 = data_input[['ALCOHOL', 'TOBAC30', 'TOBAC100', 'SMOKYRS', 'PACKSPER', 'ABUSOTHR', 'PSYCDIS', 'GDS']]

# Effect of family history
data_input_edit2 = data_input[(data_input.Age > 75.0) & (data_input.Age < 80) &
                    (data_input.Race==1) & (data_input.BMI > 25.0) & (data_input.BMI < 35.0) & (data_input.dem_idx<1)]
data_input_edit3 = data_input[ (data_input.Age > 75.0) & (data_input.Age < 80) &
                    (data_input.Race==1) & (data_input.BMI > 25.0) & (data_input.BMI < 35.0) & (data_input.dem_idx>=1)]

attr = data_input_edit2['cdr']
attr1 = data_input_edit3['cdr']
attr_all = []

attr_list = list(attr.values)
attr_list1 = list(attr1.values)
attr_all.append(attr_list)
attr_all.append(attr_list1)
print(attr_all)

colors =['black', 'r']
labels = ['den_idx = 0', 'den_idx >=1']
f, bx = plt.subplots(nrows=1, ncols=1)
bx.hist(attr_all, bins=4, normed=True, color=colors, histtype='bar', label=labels)
#bx.hist(attr1, bins=22, density=True, color='r', histtype='bar', label='CDR < 0.5')
bx.legend()
#bx.set_ylim(ztop, zbot)
#bx.invert_yaxis()
#bx.grid()
bx.locator_params(axis='x', nbins=7)
bx.set_xlabel("CDR")
bx.set_ylabel("Probability density")


plt.show()



