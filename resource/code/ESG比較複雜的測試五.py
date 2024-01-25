# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:41:08 2023

@author: crazy
"""
test1a=test1.drop(test1[test1.group_cc == 1].index)#1207*129
DID_test1a = smf.ols(formula='TESG分數 ~ C(group_bb) * C(Policy_2016)', data=test1a)
print(DID_test1a.fit().summary())



test1b=full_df[full_df.group_cc == 0]#5621*129
DID_test11 = smf.ols(formula='TESG分數 ~ C(group_bb) * C(Policy_2016)', data=test1b)
print(DID_test11.fit().summary())


# 1455 672 9143
(full_df.group_aa == 1).astype(int).sum()
(full_df.group_bb == 1).astype(int).sum()
(full_df.group_cc == 1).astype(int).sum()

full_df[(full_df.group_aa == 1) | (full_df.group_bb == 1)].shape


test1c=full_df[(full_df.group_aa == 1) | (full_df.group_bb == 1)]
DID_testv = smf.ols(formula='TESG分數 ~ C(group_bb) * C(Policy_2016)', data=test1c)
print(DID_testv.fit().summary())


full_df[full_df.D_WFN.isin(['自願','強制'])].shape
# 1589 3010 6671
full_df[full_df.D_WFN == '自願'].shape
full_df[full_df.D_WFN == '強制'].shape
full_df[full_df.D_WFN == '尚無'].shape

# 平均，針對所有子產業+年度
df_TESG = full_df.groupby(['證券代碼'])
kk = df_TESG['exam'].aggregate(['sum'])
kk = kk.reset_index()
ll = set(kk[kk['sum'] == 7].證券代碼)
full_df['exam_0'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_1'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_2'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_3'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_4'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_5'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_6'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['exam_7'] = full_df['證券代碼'].isin(ll).astype(int)
full_df['n_exam_7'] = full_df['group_dd'] - full_df['exam_7']


full_df.to_excel("okk.xlsx", index=False)

#測試五
DID_testv = smf.ols(formula='TESG分數 ~ C(exam_7) * C(Policy_2019) + {}'.format(covariates), data=full_df)
print(DID_testv.fit().summary())


full_df['exam_7'].value_counts()
