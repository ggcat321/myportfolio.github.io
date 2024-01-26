# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 18:55:42 2023

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
rc = {'font.sans-serif': ['Microsoft JhengHei']}
sns.set(font_scale=2, rc=rc)

#read data full_df for ML_qq.xlsx
real01=pd.read_excel("synth.xlsx")
full_dfff = real01.copy()
full_dfff = full_dfff.sort_values(by=['證券代碼', '年度'], ascending=[True, True])

real02=pd.read_excel("forML_qq.xlsx")
full_dff = real02.copy()
full_dff = full_dff.sort_values(by=['證券代碼', '年度'], ascending=[True, True])

real03 = pd.read_excel("okk.xlsx")
full_df = real03.copy()
full_df = full_df.sort_values(by=['證券代碼', '年度'], ascending=[True, True])

#agg functions
def pcs(df):
    
    name_list=[]
    for i in df.columns:
        name_list.append(i)
    return name_list

def n_count(a):
    return len(a)

def n_one(a):
    name_list=[]
    for i in a:
        if i ==1:
            name_list.append(i)
        return len(name_list)

def exam_pct(a):
    name_list=[]
    for i in a["永續報告書驗證_D"]:
        if i == "Y":
            name_list.append(i)
        return (len(name_list) / len(a))

def exam_count(x):
    exam_count = (x['exam'] == 1).sum()
    return exam_count



# financial
pcs(full_dfff)[116:225]
# full financial
pcs(full_dff)[155:200]

pcs(full_df)[75:120]

true_rows = full_df.iloc[:,:].dropna(axis=1).columns.tolist()


# set industry dummy
# Separate by Industries

big_filt=full_df.groupby(['年度','SASB產業'])
aa=big_filt["原始TESG分數"].aggregate(['mean',n_count])
ind_df = aa.reset_index()
# 按照產業類別分組
grouped = ind_df.groupby('SASB產業')


# Plotting
fig, ax = plt.subplots(figsize=(14, 8))
font_size = 36
for industry, group in grouped:
    x = group['年度']
    y = group['mean']/3
    plt.plot(x, y, label=industry)

plt.title('TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()



# 1. Financial Industry
fin_df = full_df[full_df.ID_金融==1]
fin_df_filt=fin_df.groupby(['年度','exam'])
fin_aa=fin_df_filt["TESG分數"].aggregate(['mean',n_count])
# 按照產業類別分組
fin_aa = fin_aa.reset_index()

grouped = fin_aa.groupby('exam')
# Plotting
fig, ax = plt.subplots(figsize=(14, 8))
font_size = 36
for industry, group in grouped:
    x = group['年度']
    y = group['mean']
    plt.plot(x, y, label=industry)
plt.title('TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()




# Overall
all_df_filt=full_df.groupby(['年度'])
all_df_filt_aa=all_df_filt["TESG分數"].aggregate(['mean',n_count])
all_df = all_df_filt_aa.reset_index()

fig, ax = plt.subplots(figsize=(14, 8))
font_size = 36

x = all_df['年度']
y = all_df['mean']
plt.plot(x, y)
plt.title('全體TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()

# The voluntary
# 2013will
pd_2013=pd.read_excel(r'C:\Users\crazy\Desktop\123\onweb\2013_onweb.xlsx')
will_2013=pd_2013.公司代號.astype(str) +str(" ") + pd_2013.公司名稱.astype(str)
# 2015will
will_2015=full_df[(full_df.will==1) & (full_df.年度==2015)].證券代碼
all_will_list = pd.concat([will_2013, will_2015]).drop_duplicates()

# Plotting
all_will_df = full_df[full_df.證券代碼.isin(all_will_list)]
all_will_df.to_excel("all_will_df.xlsx")
not_all_will_df = full_df[~full_df["證券代碼"].isin(all_will_df["證券代碼"])]
not_all_will_df.to_excel("not_all_will_df.xlsx")
big_filt01=all_will_df.groupby(['年度','SASB產業','will'])
bb=big_filt01["TESG分數"].aggregate(['mean',n_count])
qq= bb.reset_index()
grouped = qq.groupby(['年度'])

# Plotting
fig, ax = plt.subplots(figsize=(140, 80))
font_size = 36
for industry, group in grouped:
    x = group['年度']
    y = group['mean']
    plt.plot(x, y, label=industry)
plt.title('TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()


# The Never Handed In
never_ls = full_df.query("hand_in==0 & 年度==2021").證券代碼.to_list()
never_df = full_df[full_df["證券代碼"].isin(never_ls)]
full_df["never"]=full_df['證券代碼'].isin(never_ls).astype(int)
# full_df.to_excel("tableAU_df.xlsx" , index=False)


# array(['1109 信大', '2365 昆盈', '2640 大車隊', '3266 昇陽', '4163 鐿鈦', '6244 茂迪', '8027 鈦昇', '8114 振樺電', '8463 潤泰材'], dtype=object)
# 就這9間公司，與2015自願 vs never(2021) 居然有所重複，2013~2014有自願做，但2015~2021皆無繳交
full_df[(full_df["never"] & full_df["D_will_35"])==1].證券代碼.unique()
full_df["D_force"] = full_df["all_T"] - (full_df["never"] & full_df["D_will_35"])




# Combine，D_WFN
# W 239
set(true35_list)
# N 959
set(never_ls)

num_group = full_df.groupby(['年度','exam'])
kk = num_group['TESG分數'].aggregate(['mean',n_count,np.std,np.max,np.min])
kk.reset_index()
kk



full_df.iloc[0:1,120:128]

# DID...
# synth....

import statsmodels.formula.api as smf
covariates = "1"
covariates = 'C(SASB產業) + C(上市別) + ROA + 每股淨值 + 短期借款比率 + 負債總額比率'
for_year = 'Policy_2016'
for_year = 'Policy_2019'

# Test 2016 Regulations
DID_test10 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C(group_bb) + {}'.format(covariates), data=full_df)
print(DID_test10.fit().summary().tables[1])
aa= DID_test10.fit().summary().tables[1]
bb= aa.as_csv()
# Test 2016 Regulations 1
DID_test11 = smf.ols(formula='TESG分數 ~ C(group_bb) * C({}) + {}'.format(for_year, covariates), data=full_df[(full_df.group_aa == 1) | (full_df.group_bb == 1)])
print(DID_test11.fit().summary())
test1=DID_test11.fit().summary().tables[1].as_csv()
aa= DID_test11.fit().summary().tables[1]
bb= aa.as_csv()
# Test 2016 Regulations 2
DID_test12 = smf.ols(formula='TESG分數 ~ C(group_bb) * C({}) + {}'.format(for_year, covariates), data=full_df[(full_df.group_cc == 1) | (full_df.group_bb == 1)])
print(DID_test12.fit().summary())
test2=DID_test12.fit().summary().tables[1].as_csv()
aa= DID_test12.fit().summary().tables[1]
bb= aa.as_csv()
# Test 2016 Regulations
DID_test13 = smf.ols(formula='TESG分數 ~ C(group_aa) * C({}) + {}'.format(for_year, covariates), data=full_df[(full_df.group_aa == 1) | (full_df.group_cc == 1)])
print(DID_test13.fit().summary().tables[1])

# Test 2016 Voluntary all
DID_test20 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df)
print(DID_test20.fit().summary().tables[1])

# Test 2016 Voluntary 3
DID_test21 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['自願','強制'])])
print(DID_test21.fit().summary())
test2=DID_test21.fit().summary().tables[1].as_csv()
aa= DID_test21.fit().summary().tables[1]
bb= aa.as_csv()

# Test 2016 Voluntary 4
DID_test22 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','強制'])])
print(DID_test22.fit().summary())
test2=DID_test22.fit().summary().tables[1].as_csv()
aa= DID_test22.fit().summary().tables[1]
bb= aa.as_csv()

# Test 2016 Voluntary 5
DID_test23 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','自願'])])
print(DID_test23.fit().summary().tables[1])


# Test 2019 Voluntary all
DID_test30 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df)
print(DID_test30.fit().summary().tables[1])

# Test 2019 Voluntary 3
DID_test31 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['自願','強制'])])
print(DID_test31.fit().summary())
test2=DID_test31.fit().summary().tables[1].as_csv()
aa= DID_test31.fit().summary().tables[1]
bb= aa.as_csv()

# Test 2019 Voluntary 4
DID_test32 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','強制'])])
print(DID_test32.fit().summary())
test2=DID_test32.fit().summary().tables[1].as_csv()
aa= DID_test32.fit().summary().tables[1]
bb= aa.as_csv()

# Test 2019 Voluntary 5
DID_test33 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','自願'])])
print(DID_test33.fit().summary().tables[1])




# Group by ALL Industries
df_TESG = full_df.groupby(['年度','SASB子產業'])
kk = df_TESG['TESG分數'].aggregate(['mean'])
kk = kk.reset_index()
kk
Group by SASB Industries
features = full_dfff.iloc[:,3:120].columns

def weighted_average(group):
    capital_weighted = (group['新實收資本額'] / group['新實收資本額'].sum()).values
    features_weighted = (group[features] * capital_weighted.reshape(-1, 1)).sum()
    return features_weighted

# Group by SASB Industries
result = full_df.groupby(['年度','SASB子產業']).apply(weighted_average)
result = result.reset_index()
result
new_df = pd.concat([kk,result], axis=1)
new_df = new_df.iloc[:,3:]
new_df
new_df.to_excel('avg_df.xlsx',index=False)



abc = full_df[full_df['SASB產業']=="可再生資源與替代能源"]
abc.to_excel("可再生資源與替代能源.xlsx")


# Plotting - SASB Industies
text = '環境構面分數'
marker_dict = {'提煉與礦產加工': 'o', '食品與飲料': 's', '資源轉化': '+', '消費品': 'p', '公共建設': 'h', '運輸': '*', '科技與通訊': '1', '醫療保健': '2', '可再生資源與替代能源': 'x', '服務': 'd', '金融': '_'}

df_grouped = full_df.groupby(['SASB產業', '年度'])[text].mean().reset_index()
df_pivot = df_grouped.pivot(index='年度', columns='SASB產業', values=text)
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df_pivot, markers=True, markersize=12)
plt.legend(fontsize=int(FS*0.7), loc=1)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_title(text)




# Plotting-Voluntary*Examine
data = {'類型': ['尚無_無驗證', '強制_無驗證', '強制_有驗證', '自願_無驗證', '自願_有驗證'],
        '2015': [51.844, 55.490, 58.346, 61.350, 62.684],
        '2016': [52.250, 55.547, 58.378, 60.341, 62.024],
        '2017': [52.011, 55.948, 58.673, 60.852, 62.651],
        '2018': [51.827, 56.107, 59.752, 60.695, 63.237],
        '2019': [51.189, 57.159, 62.256, 62.485, 66.250],
        '2020': [51.022, 57.299, 62.392, 62.983, 65.832],
        '2021': [50.010, 58.714, 60.967, 61.887, 66.149]}
df = pd.DataFrame(data).set_index('類型')
df = df.transpose()

# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
#plt.axvline(x=1, color='r', linestyle='--')
ax.set_title('永續報告書繳交類型')



# Plotting-Easy
data = {'年度': ['強制_無驗證', '強制_有驗證', '自願_無驗證', '自願_有驗證'],
        '2015': [55.490, 58.346, 61.350, 62.684],
        '2016': [55.547, 58.378, 60.341, 62.024],
        '2017': [55.948, 58.673, 60.852, 62.651],
        '2018': [56.107, 59.752, 60.695, 63.237],
        '2019': [57.159, 62.256, 62.485, 66.250],
        '2020': [57.299, 62.392, 62.983, 65.832],
        '2021': [58.714, 60.967, 61.887, 66.149]}
df = pd.DataFrame(data).set_index('年度')
df = df.transpose()

# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)
plt.axvline(x=4, color='r', linestyle='--')

ax.set_title('永續報告書繳交類型')

# Plotting-Companies

data = {'類型': ['強制_無驗證', '強制_有驗證', '自願_無驗證', '自願_有驗證', '無繳交_無驗證'],
        '2015': [75, 119, 127, 59, 1230],
        '2016': [117, 161, 117, 52, 1163],
        '2017': [112, 175, 135, 55, 1133],
        '2018': [114, 187, 141, 68, 1100],
        '2019': [110, 192, 159, 74, 1075],
        '2020': [100, 205, 177, 102, 1026],
        '2021': [49, 260, 194, 154 ,953]}
df = pd.DataFrame(data).set_index('類型')
df = df.transpose()

# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_ylabel('公司家數', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)



# Plotting-Voulentary

data = {'類型': ['強制', '尚未', '自願'],
        '2015': [58.753, 52.599, 61.488],
        '2016': [58.150, 52.806, 60.718],
        '2017': [58.915, 52.529, 60.665],
        '2018': [59.449, 52.256, 60.746],
        '2019': [61.701, 51.474, 63.315],
        '2020': [61.803, 51.103, 62.769],
        '2021': [61.864, 50.100, 61.562]}
df = pd.DataFrame(data).set_index('類型')
df = df.transpose()

# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
#plt.axvline(x=1, color='r', linestyle='--')
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)

ax.set_title('永續報告書繳交類型', fontsize=FS)




# Plotting-Voluntary

data = {
    '年度': [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    '自願': [61.98, 61.19, 61.76, 62.09, 64.62, 64.74, 64.80],
    '尚無': [51.84, 52.25, 52.01, 51.83, 51.19, 51.02, 50.10],
    '強制': [55.94, 56.18, 56.66, 57.18, 58.77, 59.24, 60.07]
}

df = pd.DataFrame(data)
df = pd.DataFrame(data).set_index('年度')

# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.axvline(x=2019, color='r', linestyle='--')

#rc = {'font.sans-serif': ['Microsoft JhengHei']}
rc = {'font.sans-serif': ['SimHei']}
plt.legend(fontsize=FS)
ax.set_ylabel('ESG表現', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)




# Plotting-Regulation-1


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

# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.axvline(x=1, color='r', linestyle='--')
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)




# Plotting-Examine
data = {
    '年度': [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    'Exam 0': [52.73, 53.03, 52.89, 52.77, 52.58, 52.54, 51.93],
    'Exam 1': [55.81, 55.93, 56.24, 56.53, 57.43, 57.69, 59.31],
    'Exam 2': [58.48, 58.48, 58.77, 59.24, 60.10, 62.13, 62.52],
    'Exam 3': [59.63, 58.85, 60.32, 61.15, 64.03, 64.08, 63.98],
    'Exam 4': [60.18, 60.46, 61.58, 62.14, 64.56, 64.40, 66.01],
    'Exam 5': [57.51, 58.14, 59.22, 59.67, 61.95, 61.05, 60.91],
    'Exam 6': [58.96, 58.76, 59.81, 60.08, 63.80, 64.39, 64.71],
    'Exam 7': [60.93, 60.57, 61.10, 62.02, 64.59, 64.68, 64.50]
}

df = pd.DataFrame(data)
df = pd.DataFrame(data).set_index('年度')


# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.axvline(x=2019, color='r', linestyle='--')
plt.legend(fontsize=FS*0.7)
ax.set_ylabel('TESG表現', fontsize=FS)
ax.set_title('永續報告書驗證次數', fontsize=FS)




# Plotting

data = {
    '年度': [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    '上市櫃公司': [54.37, 54.56, 54.63, 54.70, 55.11, 55.15, 54.84],
}

df = pd.DataFrame(data)
df = pd.DataFrame(data).set_index('年度')


# Plotting
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS*0.7)
ax.set_ylabel('TESG表現', fontsize=FS)
ax.set_title('整體上市上櫃公司平均分數', fontsize=FS)




# 檢驗再生資源的分數表現
full_df = real03.copy()
too_new = ["1443 立益物流", "4154 樂威科-KY", "1472 三洋實業", "5205 中茂", "3219 倚強科", "6431 光麗-KY"]
rows_to_drop = full_df[full_df['證券代碼'].isin(too_new)]
filtered_df = full_df[~full_df['證券代碼'].isin(too_new)]

filtered_df.to_excel("OK.xlsx", index=False)


"""
def add_significance_stars(summary):
    df_summary = pd.read_html(summary.tables[1].as_html(), header=0, index_col=0)[0]
    p_values = results.pvalues
    stars = []
    for p in p_values:
        if p < 0.001:
            stars.append('***')
        elif p < 0.01:
            stars.append('**')
        elif p < 0.05:
            stars.append('*')
        else:
            stars.append('')
    df_summary['P>|t|'] = df_summary['P>|t|'].astype(float).map('{:.3f}'.format) + pd.Series(stars)
    return df_summary.to_string()



results = DID_test10.fit()
summary = results.summary()
summary_with_stars = add_significance_stars(summary)
print(summary_with_stars)

summary_df = pd.read_html(summary.tables[1].as_html(), header=0, index_col=0)[0]
print(summary_df)
yy = summary.tables[1].as_csv()
print(summary.tables[1])
"""