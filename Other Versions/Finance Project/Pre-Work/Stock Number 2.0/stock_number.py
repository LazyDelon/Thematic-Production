   # '''         RTM         ''' #
# ''' 股票代碼 股票名稱 股票類別  ''' #

import requests
import pandas as pd
import twstock as ts


res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")

df = pd.read_html(res.text)[0]

df = df.drop(columns=[1,2,5,6],axis=0)
df = df.drop(df.index[0:2])
df = df.drop(df.index[963:])

df.to_csv("stock_number.csv",header=0,index = "False", encoding= "utf_8_sig")