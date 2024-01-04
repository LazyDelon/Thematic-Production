import requests
import pandas as pd

res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")

df = pd.read_html(res.text)[0]

# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡


from bs4 import BeautifulSoup

soup = BeautifulSoup(res.text,"html.parser")
Last = soup.find_all("b")

Stock_Index = df.index[df[0].isin([Last[2].text.strip()])].values
Stock_Index = Stock_Index[0] - 2

df = df.drop(columns=[1,2,3,5,6], axis=0)

df = df.drop(df.index[0:2])
df = df.drop(df.index[Stock_Index:])

df.to_csv("Stock Symbol.csv", header = 0, index = False, encoding = "utf_8_sig")

# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡