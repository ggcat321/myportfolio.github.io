import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.api import anova_lm
import matplotlib.pyplot as plt
import pandas as pd
from patsy import dmatrices
import itertools as it
import random
 
 
# Load data 读取数据
df = full_df.copy()
print(df)
pcs(df)
aa = set(df.columns[129:])
bb = set(df.columns[32:77])
variate = aa|bb

 
#定义多个数组，用来分别用来添加变量，删除变量
x = []
variate_add = []
variate_del = variate.copy()
# print(variate_del)
y = random.sample(variate,3) #随机生成一个选模型，3为变量的个数
print(y)
#将随机生成的三个变量分别输入到 添加变量和删除变量的数组
for i in y:
 variate_add.append(i)
 x.append(i)
 variate_del.remove(i)
 
global aic #设置全局变量 这里选择值作为指标
formula="{}~{}".format("TESG分數","+".join(variate_add)) #将自变量名连接起来
aic=1-smf.ols(formula=formula,data=df).fit().rsquared_adj #获取随机函数的值，与后面的进行对比
print("随机化选模型为：{}~{}，对应的值为：{}".format("y","+".join(variate_add), aic))
print("\n")
 
 
 
#添加变量
def forwark():
 score_add = []
 global best_add_score
 global best_add_c
 print("添加变量")
 for c in variate_del:
  formula = "{}~{}".format("TESG分數", "+".join(variate_add+[c]))
  score = 1-smf.ols(formula = formula, data = df).fit().rsquared_adj
  score_add.append((score, c)) #将添加的变量，以及新的值一起存储在数组中
   
  print('自变量为{}，对应的值为：{}'.format("+".join(variate_add+[c]), score))
 
 score_add.sort(reverse=True) #对数组内的数据进行排序，选择出值最小的
 best_add_score, best_add_c = score_add.pop()
  
 print("最小值为：{}".format(best_add_score))
 print("\n")
 
#删除变量
def back():
 score_del = []
 global best_del_score
 global best_del_c
 print("剔除变量")
 for i in x:
 
  select = x.copy() #copy一个集合，避免重复修改到原集合
  select.remove(i)
  formula = "{}~{}".format("TESG分數","+".join(select))
  score = 1-smf.ols(formula = formula, data = df).fit().rsquared_adj
  print('自变量为{}，对应的值为：{}'.format("+".join(select), score))
  score_del.append((score, i))
 
 score_del.sort(reverse=True) #排序，方便将最小值输出
 best_del_score, best_del_c = score_del.pop() #将最小的值以及对应剔除的变量分别赋值
 print("最小值为：{}".format(best_del_score))
 print("\n")
 
print("剩余变量为：{}".format(variate_del))
forwark()
back()
 
while variate:
   
#  forwark()
#  back()
 if(aic < best_add_score < best_del_score or aic < best_del_score < best_add_score):
  print("当前回归方程为最优回归方程，为{}~{}，值为：{}".format("TESG分數","+".join(variate_add), aic))
  break
 elif(best_add_score < best_del_score < aic or best_add_score < aic < best_del_score):
  print("目前最小的值为{}".format(best_add_score))
  print('选择自变量：{}'.format("+".join(variate_add + [best_add_c]))) 
  print('\n')
  variate_del.remove(best_add_c)
  variate_add.append(best_add_c)
  print("剩余变量为：{}".format(variate_del))
  aic = best_add_score
  forwark()
 else:
  print('当前最小值为：{}'.format(best_del_score))
  print('需要剔除的变量为：{}'.format(best_del_c))
  aic = best_del_score #将值较小的选模型值赋给再接着下一轮的对比
  x.remove(best_del_c) #在原集合上剔除选模型所对应剔除的变量
  back()




"""
"""






full_df=pd.read_excel('ratio.xlsx')

import pandas as pd
import time
import statsmodels.api as sm
import numpy as np

aa = set(full_df.columns[129:])
bb = set(full_df.columns[32:77])
variate = aa|bb

start_t = time.time()
# 創建隨機的Y和X變量（示例數據）
Y = full_df['TESG分數']
X = full_df[full_df.columns[full_df.columns.isin(variate)]]

# 初始化變數和R-squared值
best_r_squared_adj = 0.0
best_formula = None

# 迴圈遍歷所有可能的組合
for i in range(len(X.columns)):
    for j in range(i+1, len(X.columns)):
        for k in range(j+1, len(X.columns)):
            for l in range(k+1, len(X.columns)):
                for m in range(l+1, len(X.columns)):
                    # 選擇四個變量進行OLS回歸
                    predictors = X[[X.columns[i], X.columns[j], X.columns[k], X.columns[l], X.columns[m]]]
                    predictors = sm.add_constant(predictors)  # 添加截距項
                    model = sm.OLS(Y, predictors).fit()
                
                    # 檢查是否有更好的R-squared值
                    if model.rsquared_adj > best_r_squared_adj:
                        best_r_squared_adj = model.rsquared_adj
                        best_formula = f"Y = {model.params['const']:.3f} + {model.params[X.columns[i]]:.3f}*{X.columns[i]} + {model.params[X.columns[j]]:.3f}*{X.columns[j]} + {model.params[X.columns[k]]:.3f}*{X.columns[k]} + {model.params[X.columns[l]]:.3f}*{X.columns[l]} + {model.params[X.columns[m]]:.3f}*{X.columns[m]}"

# 輸出最佳的迴歸式和對應的R-squared值
print("Best Regression Formula:")
print(best_formula)
print("Best R-squared_adj Value:")
print(best_r_squared_adj)

end_t = time.time()
print("run_time：%f sec" % (end_t - start_t))










