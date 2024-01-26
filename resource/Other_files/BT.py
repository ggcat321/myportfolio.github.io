# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 21:57:56 2024

@author: crazy
"""

# to buy TWN, short TXF

trades=[]
position = False
pps = []

for DATE, row in df.iterrows():
  current_price = float(row["相對強弱(絕對)"])
#S1
  if not position and (current_price>0.003752):
    trades.append({'date':row["DATE"],'空台點數':row["台指期貨(連續)"],'多摩點數':row["摩台期貨(連續)"]})
    position = True
    entry_p = current_price

  elif position and (current_price<-0.000323):
    trades.append({'date':row["DATE"],'平倉台點':row["台指期貨(連續)"],'平倉摩點':row["摩台期貨(連續)"]})
    position = False
    exit_p = current_price
    pps.append(exit_p-entry_p)

trades[0:5]

single_t = []
trades_df = pd.DataFrame(trades)

for i in range(int(len(trades_df)/2)):
  single_t.append({'in_date':trades_df.iloc[2*i]['date'],'out_date':trades_df.iloc[2*i+1]['date'],
  '台指點數':(trades_df.iloc[2*i]['空台點數']-trades_df.iloc[2*i+1]['平倉台點'])
  ,'摩台點數':(-trades_df.iloc[2*i]['多摩點數']+trades_df.iloc[2*i+1]['平倉摩點'])})
  i += 1
  
single_t_df = pd.DataFrame(single_t)
single_t_df["earn"] = single_t_df.台指點數*+200*2+single_t_df.摩台點數*100*30*3
single_t_df

#single_t_df.to_csv("777.csv",index = False, encoding = 'gbk')



# to short TWN, buy TXF
trades=[]
position = False
pps = []

for DATE, row in df.iterrows():
  current_price = float(row["相對強弱(絕對)"])
#S2
  if not position and (current_price<-0.004398):
    trades.append({'date':row["DATE"],'多台點數':row["台指期貨(連續)"],'空摩點數':row["摩台期貨(連續)"]})
    position = True
    entry_p = current_price

  elif position and (current_price>-0.000323):
    trades.append({'date':row["DATE"],'平倉台點':row["台指期貨(連續)"],'平倉摩點':row["摩台期貨(連續)"]})
    position = False
    exit_p = current_price
    pps.append(exit_p-entry_p)

single_t = []
trades_df = pd.DataFrame(trades)

for i in range(int(len(trades_df)/2)):
  single_t.append({'in_date':trades_df.iloc[2*i]['date'],'out_date':trades_df.iloc[2*i+1]['date'],
  '台指點數':(-trades_df.iloc[2*i]['多台點數']+trades_df.iloc[2*i+1]['平倉台點'])
  ,'摩台點數':(trades_df.iloc[2*i]['空摩點數']-trades_df.iloc[2*i+1]['平倉摩點'])})
  i += 1
  
single_t_df = pd.DataFrame(single_t)
single_t_df["earn"] = single_t_df.台指點數*+200*2+single_t_df.摩台點數*100*30*3
single_t_df

#trades_df.to_csv("777.csv",index = False, encoding = 'gbk')



# Strategy Backtesting

def BT(the_mean, the_std, times, AD):
  trades=[]
  position = False
  pps = []

  for i in range(len(df)-1):
    current_price = float(df["相對強弱"].iloc[i])
  #S1
    if not position and (current_price>(the_mean+times*the_std)):
      trades.append({'date':df["DATE"].iloc[i+AD],'空台點數':df["台指期貨(開)"].iloc[i+AD],'多摩點數':df["摩台期貨(開)"].iloc[i+AD]})
      position = True
      entry_p = current_price

    elif position and (current_price<the_mean):
      trades.append({'date':df["DATE"].iloc[i+AD],'平倉台點':df["台指期貨(開)"].iloc[i+AD],'平倉摩點':df["摩台期貨(開)"].iloc[i+AD]})
      position = False
      exit_p = current_price
      pps.append(exit_p-entry_p)

  trades[0:5]

  single_t = []
  trades_df = pd.DataFrame(trades)

  for i in range(int(len(trades_df)/2)):
    single_t.append({
    'in_date':trades_df.iloc[2*i]['date'],'out_date':trades_df.iloc[2*i+1]['date'],
    '台指點數':(trades_df.iloc[2*i]['空台點數']-trades_df.iloc[2*i+1]['平倉台點'])
    ,'摩台點數':(-trades_df.iloc[2*i]['多摩點數']+trades_df.iloc[2*i+1]['平倉摩點'])
    })
    i += 1
    
  single_t_df_S1 = pd.DataFrame(single_t)
  single_t_df_S1["earn"] = (single_t_df_S1.台指點數*+200*2+single_t_df_S1.摩台點數*100*30*3)
  single_t_df_S1

  trades=[]
  position = False
  pps = []

  for i in range(len(df)-1):
    current_price = float(df["相對強弱"].iloc[i])
  #S2
    if not position and (current_price<(the_mean-times*the_std)):
      trades.append({'date':df["DATE"].iloc[i+AD],'多台點數':df["台指期貨(開)"].iloc[i+AD],'空摩點數':df["摩台期貨(開)"].iloc[i+AD]})
      position = True
      entry_p = current_price

    elif position and (current_price>the_mean):
      trades.append({'date':df["DATE"].iloc[i+AD],'平倉台點':df["台指期貨(開)"].iloc[i+AD],'平倉摩點':df["摩台期貨(開)"].iloc[i+AD]})
      position = False
      exit_p = current_price
      pps.append(exit_p-entry_p)

  trades[0:5]

  single_t = []
  trades_df = pd.DataFrame(trades)

  for i in range(int(len(trades_df)/2)):
    single_t.append({
    'in_date':trades_df.iloc[2*i]['date'],'out_date':trades_df.iloc[2*i+1]['date'],
    '台指點數':(trades_df.iloc[2*i+1]['平倉台點']-trades_df.iloc[2*i]['多台點數'])
    ,'摩台點數':(trades_df.iloc[2*i]['空摩點數']-trades_df.iloc[2*i+1]['平倉摩點'])
    })
    i += 1
    
  single_t_df_S2 = pd.DataFrame(single_t)
  single_t_df_S2["earn"] = (single_t_df_S2.台指點數*200*2+single_t_df_S2.摩台點數*100*30*3)
  single_t_df_S2

  single_t_df = pd.concat([single_t_df_S1, single_t_df_S2])

  op_list = []

  po = np.array(single_t_df.out_date,dtype='datetime64')
  pi = np.array(single_t_df.in_date,dtype='datetime64')
  pp = (po-pi)/86400000000000
  tt = pp.sum()
  days = tt.astype(int)
  total_N = len(single_t_df)
  win_N = sum(1 for m in single_t_df.earn if m > 0)
  wim_M = np.round(sum(m for m in single_t_df.earn if m > 0),2)
  win_rate = np.round((win_N/total_N)*100,2)
  Loss_M = np.round(sum(m for m in single_t_df.earn if m < 0),2)
  Win_Avg = np.round((wim_M/total_N),2)
  loss_Avg = np.round((Loss_M/total_N),2)
  days_avg = np.round(days/total_N,2)
  the_ratio = np.round((wim_M/Loss_M*-1),2)
  MAX_WIN = single_t_df.earn.max()
  MAX_LOSS = single_t_df.earn.min()
  TA = np.round((wim_M/total_N)*100,2)
  To_M = np.round(sum(m for m in single_t_df.earn),2)

  op_list = [{"N_std":times,"Trades":total_N,"Win Rate":win_rate,"Days_Avg.":days_avg,"Win Avg":Win_Avg,
              "Loss_Avg.":loss_Avg,"Ratio":the_ratio,"Max_win":MAX_WIN,"Max_loss":MAX_LOSS,"Avg. Earn":TA,"Win Money":wim_M, "Total_Money":To_M}]
  op_list = pd.DataFrame(op_list)
  print(f"Win Rate : {win_rate:.2f}%")
  print(f"Win Money : {wim_M:.2f}")
  print(f"Win Avg. : {Win_Avg:.2f}")

  return op_list



# result

big_df = pd.DataFrame()
for i in range(25):
  k = (i+1)/10
  temp = BT(the_mean, the_std, k)
  big_df = pd.concat([big_df, temp], axis = 0)