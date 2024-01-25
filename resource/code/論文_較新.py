# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 21:22:16 2023

@author: crazy
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font_scale=2)
sns.set_theme(style = "darkgrid")
os.chdir(r"C:\Users\crazy\Desktop\碩士論文\123")
zz=(16,12)
aa=1.2
FS=24
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
pd.set_option("display.precision", 3)

# 繪製折線圖 - D_WFN

data = {
    '年度': [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    '自願': [61.98, 61.19, 61.76, 62.09, 64.62, 64.74, 64.80],
    '尚無': [51.84, 52.25, 52.01, 51.83, 51.19, 51.02, 50.10],
    '強制': [55.94, 56.18, 56.66, 57.18, 58.77, 59.24, 60.07]
}

df = pd.DataFrame(data)
df = pd.DataFrame(data).set_index('年度')


# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.axvline(x=2019, color='r', linestyle='--')

rc = {'font.sans-serif': ['Microsoft JhengHei']}

plt.legend(fontsize=FS)

sns.set(font_scale=2, rc=rc)
ax.set_ylabel('ESG表現', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)


real03 = pd.read_excel("okk.xlsx")
full_df = real03.copy()
full_df = full_df.sort_values(by=['證券代碼', '年度'], ascending=[True, True])


import statsmodels.formula.api as smf
#測試比率
Rtest01 = smf.ols(formula='環境構面揭露項_分數 ~ C(exam)', data=full_df)
print(Rtest01.fit().summary())

Rtest02 = smf.ols(formula='社會構面揭露項_分數 ~ C(exam)', data=full_df)
print(Rtest02.fit().summary())

Rtest03 = smf.ols(formula='公司治理構面揭露項_分數 ~ C(exam)', data=full_df)
print(Rtest03.fit().summary())

Rtest04 = smf.ols(formula='n_exam_7 ~ C(exam)', data=full_df)
print(Rtest04.fit().summary())


#DID 時間縮短一點的
covariates = "1"
covariates = 'C(SASB產業) + C(上市別) + ROA + 每股淨值 + 短期借款比率 + 負債總額比率'
for_year = 'Policy_2016'
for_year = 'Policy_2019'
# 測試2016法規_ab 測試一
DID_test11 = smf.ols(formula='TESG分數 ~ C(group_bb) * C({}) + {}'.format(for_year, covariates), data=full_df[((full_df.group_aa == 1) | (full_df.group_bb == 1)) & full_df.年度.isin([2015,2016,2017,2018,2019,2020,2021])])
print(DID_test11.fit().summary())
test11 = DID_test11.fit().summary().tables[1].as_csv()
aa1 = DID_test11.fit().summary().tables[1]
bb1 = aa1.as_csv()
# 測試2016法規_bc 測試一
DID_test12 = smf.ols(formula='TESG分數 ~ C(group_bb) * C({}) + {}'.format(for_year, covariates), data=full_df[((full_df.group_bb == 1) | (full_df.group_cc == 1)) & full_df.年度.isin([2015,2016,2017,2018,2019,2020,2021])])
print(DID_test12.fit().summary())
test12 = DID_test12.fit().summary().tables[1].as_csv()
aa2 = DID_test12.fit().summary().tables[1]
bb2 = aa2.as_csv()
# 測試2016法規_ab 測試一 + special
DID_test11 = smf.ols(formula='TESG分數 ~ C(special) * C({}) + {}'.format(for_year, covariates), data=full_df[((full_df.group_aa == 1) | (full_df.group_bb == 1)) & full_df.年度.isin([2015,2016,2017,2018,2019,2020,2021])])
print(DID_test11.fit().summary())
test11 = DID_test11.fit().summary().tables[1].as_csv()
aa1 = DID_test11.fit().summary().tables[1]
bb1 = aa1.as_csv()
# 測試2016法規_bc 測試一 + special
DID_test12 = smf.ols(formula='TESG分數 ~ C(special) * C({}) + {}'.format(for_year, covariates), data=full_df[((full_df.group_bb == 1) | (full_df.group_cc == 1)) & full_df.年度.isin([2015,2016,2017,2018,2019,2020,2021])])
print(DID_test12.fit().summary())
test12 = DID_test12.fit().summary().tables[1].as_csv()
aa2 = DID_test12.fit().summary().tables[1]
bb2 = aa2.as_csv()













#time 
# 測試2016法規_ab_diff
DID_test113 = smf.ols(formula='TESG分數 ~ C(group_bb) * C(年度) + {}'.format(covariates), data=full_df[(full_df.group_aa == 1) | (full_df.group_bb == 1)])
print(DID_test113.fit().summary())
# 測試2016法規_bc_diff
DID_test123 = smf.ols(formula='TESG分數 ~ C(group_bb) * C(年度) + {}'.format(covariates), data=full_df[(full_df.group_cc == 1) | (full_df.group_bb == 1)])
print(DID_test123.fit().summary())



# 繪製折線圖 - 法規一測試結果折線圖


data = {'類型': ['group_a', 'group_b', 'group_c'],
        '2015': [58.686, 58.119, 53.432],
        '2016': [58.420, 57.861, 53.717],
        '2017': [58.420, 58.660, 53.646],
        '2018': [59.776, 58.713, 53.591],
        '2019': [61.921, 61.202, 53.559],
        '2020': [62.125, 61.378, 53.563],
        '2021': [61.453, 62.861, 53.173]}
df = pd.DataFrame(data).set_index('類型')
df = df.transpose()

# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.axvline(x=1, color='r', linestyle='--')
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)


dataF = {'類型': ['ab_diff', 'bc_diff'],
        '2015': [0, 0],
        '2016': [0.008, -0.543],
        '2017': [0.807, 0.327],
        '2018': [-0.496, 0.435],
        '2019': [-0.152, 2.956],
        '2020': [-0.180, 3.128],
        '2021': [1.975, 5.001]}

dff = pd.DataFrame(dataF).set_index('類型')
dff = dff.transpose()

nn=1.96
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
x_data = [2015,2016,2017,2018,2019,2020,2021]
y1_data = dff.ab_diff.values.tolist()
y2_data = dff.bc_diff.values.tolist()
y1_err = (np.asarray([0,1.184,1.184,1.185,1.188,1.186,1.186])*nn).tolist()
y2_err = (np.asarray([0,1.021,1.023,1.026,1.031,1.028,1.028])*nn).tolist()
plt.errorbar(x_data, y1_data, yerr = y1_err, fmt='g-o', label = 'ab_diff', ms=10)
plt.errorbar(x_data, y2_data, yerr = y2_err, fmt='b-x', label = 'bc_diff', ms=16)
plt.axvline(x=2016, color='r', linestyle='--')
plt.axhline(y=0, color='black')
plt.legend(fontsize=FS, loc=2)
ax.set_ylabel('平均TESG分數差異', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)
ax.set_title('DID - 交乘效果, alpha = 0.05', fontsize=FS)
plt.show()

