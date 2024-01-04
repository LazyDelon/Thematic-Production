 # '''         Beta 1.0        ''' #
# ''' 股票代碼 股票名稱 股票類別  ''' #

import sqlite3
import pandas as pd
import twstock as ts

''' 資料集：抓取台股所有上市代碼 '''
df = pd.DataFrame(ts.twse)  

''' 刪除不要的行 '''
df = df.drop(df.index[7:8])
df = df.drop(df.index[3:6])
df = df.drop(df.index[0:2])
data = df.values # 將 Dataframe 轉成 2D Numpy array

# 找到數據的 key
index1 = list(df.keys())

#行列互換，再利用map函數將zip內的元組轉列表
data = list(map(list, zip(*data)))
data = pd.DataFrame(data, index=index1)
data = data.drop(data.index[931:16195]) # 刪除權證和ETF
data.to_csv("stock_number.csv",header=0, encoding= "utf_8_sig")

name = ['Stock_Code', 'Stock_Name', 'Industry']
df = pd.read_csv("stock_number.csv", names=name, encoding="utf_8_sig") 
df.to_csv("stock_number.csv", encoding= "utf_8_sig", header=0, index=0)

conn = sqlite3.connect("stockid.db")
name = ['Stock_Code', 'Stock_Name', 'Industry']
df = pd.read_csv("stock_number.csv", names=name, header=0, encoding="utf_8_sig") 
df.to_sql("stockid", conn, if_exists="append", index=False)
