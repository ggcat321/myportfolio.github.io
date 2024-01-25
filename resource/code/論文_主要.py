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

#agg函數們
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
# 按照產業類別分組


big_filt=full_df.groupby(['年度','SASB產業'])
aa=big_filt["原始TESG分數"].aggregate(['mean',n_count])
ind_df = aa.reset_index()
# 按照產業類別分組
grouped = ind_df.groupby('SASB產業')


# 畫出折線圖，由grouped後的新表格後才能做圖
fig, ax = plt.subplots(figsize=(14, 8))
font_size = 36
for industry, group in grouped:
    x = group['年度']
    y = group['mean']/3
    plt.plot(x, y, label=industry)

# 加入標題、X軸標籤、Y軸標籤和圖例
plt.title('TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()



# 細分產業 1. 金融
fin_df = full_df[full_df.ID_金融==1]
fin_df_filt=fin_df.groupby(['年度','exam'])
fin_aa=fin_df_filt["TESG分數"].aggregate(['mean',n_count])
# 按照產業類別分組
fin_aa = fin_aa.reset_index()

grouped = fin_aa.groupby('exam')
# 畫出折線圖，由grouped後的新表格後才能做圖(後可由reset_index()處理之)
fig, ax = plt.subplots(figsize=(14, 8))
font_size = 36
for industry, group in grouped:
    x = group['年度']
    y = group['mean']
    plt.plot(x, y, label=industry)
# 加入標題、X軸標籤、Y軸標籤和圖例
plt.title('TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()








# 大全體
all_df_filt=full_df.groupby(['年度'])
all_df_filt_aa=all_df_filt["TESG分數"].aggregate(['mean',n_count])
all_df = all_df_filt_aa.reset_index()

# 畫出折線圖
fig, ax = plt.subplots(figsize=(14, 8))
font_size = 36

x = all_df['年度']
y = all_df['mean']
plt.plot(x, y)
# 加入標題、X軸標籤、Y軸標籤和圖例
plt.title('全體TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()

# 一開始就自願者
# 2013will
pd_2013=pd.read_excel(r'C:\Users\crazy\Desktop\123\onweb\2013_onweb.xlsx')
will_2013=pd_2013.公司代號.astype(str) +str(" ") + pd_2013.公司名稱.astype(str)
# 2015will
will_2015=full_df[(full_df.will==1) & (full_df.年度==2015)].證券代碼
all_will_list = pd.concat([will_2013, will_2015]).drop_duplicates()

# 畫出折線圖
all_will_df = full_df[full_df.證券代碼.isin(all_will_list)]
all_will_df.to_excel("all_will_df.xlsx")
not_all_will_df = full_df[~full_df["證券代碼"].isin(all_will_df["證券代碼"])]
not_all_will_df.to_excel("not_all_will_df.xlsx")
big_filt01=all_will_df.groupby(['年度','SASB產業','will'])
bb=big_filt01["TESG分數"].aggregate(['mean',n_count])
qq= bb.reset_index()
grouped = qq.groupby(['年度'])

# 畫出折線圖，由grouped後的新表格後才能做圖(後可由reset_index()處理之)
fig, ax = plt.subplots(figsize=(140, 80))
font_size = 36
for industry, group in grouped:
    x = group['年度']
    y = group['mean']
    plt.plot(x, y, label=industry)
# 加入標題、X軸標籤、Y軸標籤和圖例
plt.title('TESG分數隨時間變化')
plt.xlabel('年度')
plt.ylabel('TESG分數')
plt.legend()
plt.grid()
plt.show()



# 檢驗"自願者的效果與表現"

# true will 2013~2014
true34=pd.read_excel('will_list_2013_2014.xlsx')
true34["證券代碼"]=true34.公司代號.astype(str) +str(" ") + true34.公司名稱.astype(str)
true34 = true34.drop_duplicates()
true34_list=true34["證券代碼"].reindex()
will_df_2013_2014=full_df[full_df["證券代碼"].isin(true34_list)]
will_df_2013_2014.to_excel('will_df_2013_2014.xlsx')

# true will 2013~2015
true35=pd.read_excel('will_list_2013_2015.xlsx')
true35["證券代碼"]=true35.公司代號.astype(str) +str(" ") + true35.公司名稱.astype(str)
true35 = true35.drop_duplicates()
true35_list=true35["證券代碼"].reindex()
will_df_2013_2015=full_df[full_df["證券代碼"].isin(true35_list)]
will_df_2013_2015.to_excel('will_df_2013_2015.xlsx')


full_df["D_will_35"]=full_df['證券代碼'].isin(true35_list).astype(int)
full_df["D_will_34"]=full_df['證券代碼'].isin(true34_list).astype(int)
full_df["D_will_35"].value_counts()
full_df["D_will_34"].value_counts()

#{'2035 唐榮公司', '6579 研揚', '6803 崑鼎投控'}
set(true35_list)-set(full_df['證券代碼'])
#{'6803 崑鼎投控'}
set(true34_list)-set(full_df['證券代碼'])



full_df.to_excel("tableu_df.xlsx", index=False)


# 標定 永遠的未繳交者
never_ls = full_df.query("hand_in==0 & 年度==2021").證券代碼.to_list()
never_df = full_df[full_df["證券代碼"].isin(never_ls)]
full_df["never"]=full_df['證券代碼'].isin(never_ls).astype(int)
# full_df.to_excel("tableAU_df.xlsx" , index=False)


# array(['1109 信大', '2365 昆盈', '2640 大車隊', '3266 昇陽', '4163 鐿鈦', '6244 茂迪', '8027 鈦昇', '8114 振樺電', '8463 潤泰材'], dtype=object)
# 就這9間公司，與2015自願 vs never(2021) 居然有所重複，2013~2014有自願做，但2015~2021皆無繳交
full_df[(full_df["never"] & full_df["D_will_35"])==1].證券代碼.unique()
full_df["D_force"] = full_df["all_T"] - (full_df["never"] & full_df["D_will_35"])




# 合併，D_WFN
# W 239
set(true35_list)
# N 959
set(never_ls)

# TW 230 ok
TW = set(true35_list) - set(full_df[(full_df["never"] & full_df["D_will_35"])==1].證券代碼.unique())
# TN 959 ok
TN = set(never_ls)
# TF 430 should be 427...
TF = (set(full_df.證券代碼.unique()) - TW) - TN
# TA 1616
TA = set(full_df.證券代碼.unique())

def set_value(x):
    if x in TW:
        return '自願'
    elif x in TN:
        return '尚無'
    elif x in TF:
        return '強制'
    else:
        return 0

full_df['D_WFN'] = full_df['證券代碼'].apply(lambda x: set_value(x))

df_exam = full_df.query("exam==1").證券代碼.unique()
condi01= full_df['D_WFN']=='自願'
condi02= full_df['exam']==0
qqq = full_df[condi01&condi02]
# ['2718 晶悅', '2726 雅茗-KY', '3447 展達', '4942 嘉彰', '6244 茂迪','9943 好樂迪']
# 以上6間居然有尚無繳交，卻有exam???
# 2718 晶悅，因為2020餐飲收入占比過半，所以強制交了一年。
# 2726 雅茗-KY 15~18，原因同上。且有驗證。且有驗證
# 3447 展達 2020自願了一年。且有驗證。
# 4942 嘉彰 2018自願了一年。且有驗證。
# 6244 茂迪 怪，15~16自願，17~19強制，20~21未繳交。股本原因強制。15~18驗證。
# 9943 好樂迪 15~20強制，且都有驗證，餐飲收入占比過半。

#檢查驗證用
full_df[full_df['證券代碼']=='2718 晶悅'].exam


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

# 測試2016法規_all_abc
DID_test10 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C(group_bb) + {}'.format(covariates), data=full_df)
print(DID_test10.fit().summary().tables[1])
aa= DID_test10.fit().summary().tables[1]
bb= aa.as_csv()
# 測試2016法規_ab 測試一
DID_test11 = smf.ols(formula='TESG分數 ~ C(group_bb) * C({}) + {}'.format(for_year, covariates), data=full_df[(full_df.group_aa == 1) | (full_df.group_bb == 1)])
print(DID_test11.fit().summary())
test1=DID_test11.fit().summary().tables[1].as_csv()
aa= DID_test11.fit().summary().tables[1]
bb= aa.as_csv()
# 測試2016法規_bc 測試二
DID_test12 = smf.ols(formula='TESG分數 ~ C(group_bb) * C({}) + {}'.format(for_year, covariates), data=full_df[(full_df.group_cc == 1) | (full_df.group_bb == 1)])
print(DID_test12.fit().summary())
test2=DID_test12.fit().summary().tables[1].as_csv()
aa= DID_test12.fit().summary().tables[1]
bb= aa.as_csv()
# 測試2016法規_ac
DID_test13 = smf.ols(formula='TESG分數 ~ C(group_aa) * C({}) + {}'.format(for_year, covariates), data=full_df[(full_df.group_aa == 1) | (full_df.group_cc == 1)])
print(DID_test13.fit().summary().tables[1])

# 測試2016自願_all_abc
DID_test20 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df)
print(DID_test20.fit().summary().tables[1])

# 測試2016自願_all_ab 測試三
DID_test21 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['自願','強制'])])
print(DID_test21.fit().summary())
test2=DID_test21.fit().summary().tables[1].as_csv()
aa= DID_test21.fit().summary().tables[1]
bb= aa.as_csv()

# 測試2016自願_all_bc 測試四
DID_test22 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','強制'])])
print(DID_test22.fit().summary())
test2=DID_test22.fit().summary().tables[1].as_csv()
aa= DID_test22.fit().summary().tables[1]
bb= aa.as_csv()

# 測試2016自願_all_ac
DID_test23 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','自願'])])
print(DID_test23.fit().summary().tables[1])


# 測試2019自願_all_abc
DID_test30 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df)
print(DID_test30.fit().summary().tables[1])

# 測試2019自願_all_ab 測試三
DID_test31 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['自願','強制'])])
print(DID_test31.fit().summary())
test2=DID_test31.fit().summary().tables[1].as_csv()
aa= DID_test31.fit().summary().tables[1]
bb= aa.as_csv()

# 測試2019自願_all_bc 測試四
DID_test32 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','強制'])])
print(DID_test32.fit().summary())
test2=DID_test32.fit().summary().tables[1].as_csv()
aa= DID_test32.fit().summary().tables[1]
bb= aa.as_csv()

# 測試2019自願_all_ac
DID_test33 = smf.ols(formula='TESG分數 ~ C(D_WFN) * C({}) + {}'.format(for_year, covariates), data=full_df[full_df.D_WFN.isin(['尚無','自願'])])
print(DID_test33.fit().summary().tables[1])


# 逐步回歸後，比較好的候選X's 為:
"""
all

淨值_資產_比率+其他綜合損益OCI+本期產生現金流量+
ROA+每股淨值+總資產報酬成長率+資產總額+稅率+營業收入毛額+
TobinsQ+總資產成長率+ROE+資本公積合計+每股盈餘+短期借款+總負債_總淨值_比率+
商譽及無形資產合計+應付帳款及票據+期初現金及約當現金+保留盈餘+合併總損益+
所得稅費用+期末現金及約當現金+本期綜合損益總額
"""
strr = "淨值_資產_比率+其他綜合損益OCI+本期產生現金流量+ROA+每股淨值+總資產報酬成長率+資產總額+稅率+營業收入毛額+TobinsQ+總資產成長率+ROE+資本公積合計+每股盈餘+短期借款+總負債_總淨值_比率+商譽及無形資產合計+應付帳款及票據+期初現金及約當現金+保留盈餘+合併總損益+所得稅費用+期末現金及約當現金+本期綜合損益總額"
x_ls = strr.split('+')

strr01 = "ROA+每股淨值"

# test
DID_test20 = smf.ols(formula='{} ~ TESG分數'.format(strr), data=full_df)
print(DID_test20.fit().summary())

"""
"""

full_df["總權益"] = (1-full_df["負債比率"])*full_df["資產總額"] 
full_df["現金及約當現金比率"] = full_df["現金及約當現金"]/full_df["資產總額"] 
full_df["應收帳款及票據比率"] = full_df["應收帳款及票據"]/full_df["資產總額"] 
full_df["不動產廠房及設備比率"] = full_df["不動產廠房及設備"]/full_df["資產總額"] 
full_df["商譽及無形資產合計比率"] = full_df["商譽及無形資產合計"]/full_df["資產總額"] 
full_df["非流動資產比率"] = full_df["非流動資產"]/full_df["資產總額"] 
full_df["流動資產比率"] = 1 - full_df["非流動資產比率"]
full_df["短期借款比率"] = full_df["短期借款"]/full_df["資產總額"] 
full_df["應付帳款及票據比率"] = full_df["應付帳款及票據"]/full_df["資產總額"] 
full_df["其他應付款比率"] = full_df["其他應付款"]/full_df["資產總額"] 
full_df["當期所得稅負債比率"] = full_df["當期所得稅負債"]/full_df["資產總額"] 
full_df["遞延所得稅比率"] = full_df["遞延所得稅"]/full_df["資產總額"] 
full_df["負債總額比率"] = full_df["負債總額"]/full_df["資產總額"] 
full_df["資本公積合計比率"] = full_df["資本公積合計"]/full_df["資產總額"] 
full_df["保留盈餘比率"] = full_df["保留盈餘"]/full_df["資產總額"] 
full_df["其他權益比率"] = full_df["其他權益"]/full_df["資產總額"] 
full_df["股東權益總額比率"] = full_df["股東權益總額"]/full_df["資產總額"] 
full_df["本期產生現金流量比率"] = full_df["本期產生現金流量"]/full_df["資產總額"] 
full_df["期初現金及約當現金比率"] = full_df["期初現金及約當現金"]/full_df["資產總額"] 
full_df["期末現金及約當現金比率"] = full_df["期末現金及約當現金"]/full_df["資產總額"] 

full_df["營業收入毛額比率"] = full_df["營業收入毛額"]/full_df["資產總額"] 

full_df["營業費用比率"] = full_df["營業費用"]/full_df["營業收入毛額"] 
full_df["稅前淨利比率"] = full_df["稅前淨利"]/full_df["營業收入毛額"] 
full_df["所得稅費用比率"] = full_df["所得稅費用"]/full_df["營業收入毛額"] 
full_df["合併總損益比率"] = full_df["合併總損益"]/full_df["營業收入毛額"] 
full_df["其他綜合損益OCI比率"] = full_df["其他綜合損益OCI"]/full_df["營業收入毛額"] 
full_df["本期綜合損益總額比率"] = full_df["本期綜合損益總額"]/full_df["營業收入毛額"] 
full_df["綜合損益歸屬母公司比率"] = full_df["綜合損益歸屬母公司"]/full_df["營業收入毛額"] 
full_df["綜合損益歸屬非控制權益比率"] = full_df["綜合損益歸屬非控制權益"]/full_df["營業收入毛額"]

"""
"""







full_df.to_excel("ratio.xlsx")




all_fin = full_df.columns[32:77].to_list()
new_fin = full_df.columns[129:158].to_list()
total_fin = all_fin + new_fin


fin_df = pd.DataFrame()
for i in total_fin:
    DID = smf.ols(formula='{} ~ TESG分數'.format(i), data=full_df[full_df.年度==2021])
    fin_df = pd.concat([fin_df, DID.fit().tvalues], axis = 1)
    
fin_df.loc[-1] = total_fin



DID = smf.ols(formula='營業費用比率 ~ TESG分數', data=full_df)
fin_df = pd.concat([fin_df, DID.fit().tvalues], axis = 1)



#Import packages
from SyntheticControlMethods import Synth

#Import data
data = full_dfff.copy()


#Fit classic Synthetic Control
sc = Synth(data, "TESG分數", "證券代碼", "年度", 2016, "3447 展達", pen=0)
sc.plot(["original", "pointwise", "cumulative"], treated_label="3447 展達", synth_label="Synthetic West Germany", treatment_label="German Reunification")













# 平均，針對所有子產業+年度
df_TESG = full_df.groupby(['年度','SASB子產業'])
kk = df_TESG['TESG分數'].aggregate(['mean'])
kk = kk.reset_index()
kk
# 按照 SASB 產業分组，並計算加權平均
features = full_dfff.iloc[:,3:120].columns

def weighted_average(group):
    capital_weighted = (group['新實收資本額'] / group['新實收資本額'].sum()).values
    features_weighted = (group[features] * capital_weighted.reshape(-1, 1)).sum()
    return features_weighted

# 使用 groupby 方法按照 'SASB產業' 欄位進行分組，然後對每個分組應用自定義的函數
result = full_df.groupby(['年度','SASB子產業']).apply(weighted_average)
result = result.reset_index()
result
new_df = pd.concat([kk,result], axis=1)
new_df = new_df.iloc[:,3:]
new_df
new_df.to_excel('avg_df.xlsx',index=False)



abc = full_df[full_df['SASB產業']=="可再生資源與替代能源"]
abc.to_excel("可再生資源與替代能源.xlsx")



# 可D _ to end
full_df.SASB產業.unique()
grouped = full_df.groupby('SASB產業')


# 繪製折線圖 - SASB產業折現突ok
text = '環境構面分數'
marker_dict = {'提煉與礦產加工': 'o', '食品與飲料': 's', '資源轉化': '+', '消費品': 'p', '公共建設': 'h', '運輸': '*', '科技與通訊': '1', '醫療保健': '2', '可再生資源與替代能源': 'x', '服務': 'd', '金融': '_'}

df_grouped = full_df.groupby(['SASB產業', '年度'])[text].mean().reset_index()
df_pivot = df_grouped.pivot(index='年度', columns='SASB產業', values=text)
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df_pivot, markers=True, markersize=12)
plt.legend(fontsize=int(FS*0.7), loc=1)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_title(text)




# 折線圖 可用分數-全D_WFN*Exam
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

# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
#plt.axvline(x=1, color='r', linestyle='--')
ax.set_title('永續報告書繳交類型')



# 折線圖 可用分數_上突縮減版
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

# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)
plt.axvline(x=4, color='r', linestyle='--')

ax.set_title('永續報告書繳交類型')

# 繪製折線圖 - 完整版-公司家數

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

# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_ylabel('公司家數', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)


# 繪製折線圖 - 縮減版-公司家數

data = {'年度': ['強制_無驗證', '強制_有驗證', '自願_無驗證', '自願_有驗證'],
        '2015': [75, 119, 127, 59],
        '2016': [117, 161, 117, 52],
        '2017': [112, 175, 135, 55],
        '2018': [114, 187, 141, 68],
        '2019': [110, 192, 159, 74],
        '2020': [100, 205, 177, 102],
        '2021': [49, 260, 194, 154]}
df = pd.DataFrame(data).set_index('年度')
df = df.transpose()

# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)
ax.set_ylabel('公司家數', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)




# 繪製折線圖 - 原始D_自願強制

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

# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
#plt.axvline(x=1, color='r', linestyle='--')
plt.legend(fontsize=FS)
ax.set_ylabel('TESG分數', fontsize=FS)
ax.set_xlabel('年度', fontsize=FS)

ax.set_title('永續報告書繳交類型', fontsize=FS)




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

#rc = {'font.sans-serif': ['Microsoft JhengHei']}
rc = {'font.sans-serif': ['SimHei']}
plt.legend(fontsize=FS)
ax.set_ylabel('ESG表現', fontsize=FS)
ax.set_title('永續報告書繳交類型', fontsize=FS)




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




# 繪製折線圖 - 全勤驗證表現

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


# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.axvline(x=2019, color='r', linestyle='--')
plt.legend(fontsize=FS*0.7)
ax.set_ylabel('TESG表現', fontsize=FS)
ax.set_title('永續報告書驗證次數', fontsize=FS)




# 繪製折線圖 - 整體大會圖

data = {
    '年度': [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    '上市櫃公司': [54.37, 54.56, 54.63, 54.70, 55.11, 55.15, 54.84],
}

df = pd.DataFrame(data)
df = pd.DataFrame(data).set_index('年度')


# 繪圖
fig, ax = plt.subplots(figsize=(14*aa, 8*aa))
sns.lineplot(data=df, markers=True, markersize=12)
plt.legend(fontsize=FS*0.7)
ax.set_ylabel('TESG表現', fontsize=FS)
ax.set_title('整體上市上櫃公司平均分數', fontsize=FS)








# 檢驗再生資源的分數表現


# 1443 立益物流 2021 消費品 轉 運輸*
# 4154 樂威科-KY 2021 食品 轉 消費品*
# 1472 三洋實業	2021 消費品* 轉 公共建設
# 5205 中茂	2021 資源轉化* 轉 公共建設
# 3219 倚強科 2015 科技與通訊* 轉 資源轉化
# 6431 光麗-KY 2015 科技與通訊 轉 消費品*

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


#這是測驗WFN*EXAM者 測驗六
conditions = [
    (full_df['D_WFN'] == '自願') & (full_df['exam'] == 1),
    (full_df['D_WFN'] == '自願') & (full_df['exam'] == 0),
    (full_df['D_WFN'] == '強制') & (full_df['exam'] == 1),
    (full_df['D_WFN'] == '強制') & (full_df['exam'] == 0)
]
choices = ['自願_驗證','自願_無驗證','強制_驗證','強制_無驗證']

full_df['test'] = np.select(conditions, choices, default='純尚無繳交')

full_df['test'].value_counts()
# 測試overall 測試六
covariates = 1
covariates = 'C(SASB產業) + C(上市別) + ROA + 每股淨值 + 短期借款比率 + 負債總額比率'

DID_test00 = smf.ols(formula='TESG分數 ~ C(test) * C(Policy_2019) + {}'.format(covariates), data=full_df[(full_df.test == '自願_無驗證') | (full_df.test == '自願_驗證') | (full_df.test == '強制_無驗證') | (full_df.test == '強制_驗證')])
print(DID_test00.fit().summary())
test2=DID_test00.fit().summary().tables[1].as_csv()
aa= DID_test00.fit().summary().tables[1]
bb= aa.as_csv()


#測試五
DID_testv = smf.ols(formula='TESG分數 ~ C(exam_7) * C(Policy_2019) + 新實收資本額 + {}'.format(covariates), data=full_df)
print(DID_testv.fit().summary())
aa= DID_testv.fit().summary().tables[1]
bb= aa.as_csv()

full_df['exam_7'].value_counts()
