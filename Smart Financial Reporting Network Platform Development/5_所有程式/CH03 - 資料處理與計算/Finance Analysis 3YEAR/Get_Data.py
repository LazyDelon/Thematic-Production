import os
import csv
import sqlite3
import numpy as np
import pandas as pd
from glob import glob
from collections import OrderedDict


def Get_StockNumber(): 

    Results = [] 

    try:
        with open('Stock Symbol.csv', encoding="utf-8-sig") as File: 
            
            F_Read = File.readlines()

            for Stock_List in F_Read: 
            
                S = Stock_List.replace("\u3000", ",")
                S = S.split(',')

                Results.append([S[0].strip(), str(S[1].strip()), str(S[2].strip())]) 

    except:
        print('讀不到')

    return Results

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Get_Finance(Number):

    # Path = "C:\\Senior Project\\"
    Path = "C:\\Users\\USER\\Desktop\\"

    Data_File = pd.read_csv(Path + "Result_Y.csv", encoding="utf_8_sig")
    Data_File['判斷'] = Data_File['會計項目'].astype(str) + "_" + Data_File['股票代碼'].values.astype(str)
    Data_File.to_csv(Path + "Result_Y.csv", index=False, encoding="utf_8_sig")

    with open(Path + "Result_3Y.csv", 'a+', newline="", encoding='utf-8-sig') as File:
         
        File_R = csv.writer(File)

        with open(Path + "Result_3Y.csv", 'r', newline="", encoding='utf-8-sig') as File:
        
            render = csv.reader(File)

            if not [row for row in render]:

                File_R.writerow(["股票代碼"])
                File_R.writerow([(Number)])
            else:
                File_R.writerow([(Number)])

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def GetResult(Number): 

    # Path = "C:\\Senior Project\\"
    Path = "C:\\Users\\USER\\Desktop\\"

    Data_File = pd.read_csv(Path + "Result_Y.csv", index_col="判斷", encoding="utf_8_sig")   
    FResult = pd.read_csv(Path + "Result_3Y.csv", index_col="股票代碼", encoding="utf_8_sig")

    # ▌▌▌▌▌▌ ◎ 流動比率  

    FResult.loc[int(Number), '流動比率_3Y'] = Data_File.loc[str("2019_" + Number), "流動比率"] + Data_File.loc[str("2020_" + Number), "流動比率"] + Data_File.loc[str("2021_" + Number), "流動比率"]
    FResult.loc[int(Number), '流動比率_3Y'] = FResult.loc[int(Number), '流動比率_3Y'] / 3
    FResult.loc[int(Number), '流動比率_3Y'] = round(FResult.loc[int(Number), '流動比率_3Y'], 2)
    
    
    # ▌▌▌▌▌▌ ◎ 速動比率  

    FResult.loc[int(Number), '速動比率_3Y'] = Data_File.loc[str("2019_" + Number), "速動比率"] + Data_File.loc[str("2020_" + Number), "速動比率"] + Data_File.loc[str("2021_" + Number), "速動比率"]
    FResult.loc[int(Number), '速動比率_3Y'] = FResult.loc[int(Number), '速動比率_3Y'] / 3
    FResult.loc[int(Number), '速動比率_3Y']  = round(FResult.loc[int(Number), '速動比率_3Y'], 2)

    # ▌▌▌▌▌▌ ◎ 利息保障倍數 

    FResult.loc[int(Number), '利息保障倍數_3Y'] = Data_File.loc[str("2019_" + Number), "利息保障倍數"] + Data_File.loc[str("2020_" + Number), "利息保障倍數"] + Data_File.loc[str("2021_" + Number), "利息保障倍數"]
    FResult.loc[int(Number), '利息保障倍數_3Y'] = FResult.loc[int(Number), '利息保障倍數_3Y'] / 3
    FResult.loc[int(Number), '利息保障倍數_3Y']  = round(FResult.loc[int(Number), '利息保障倍數_3Y'], 2)
   
    # ▌▌▌▌▌▌ ◎ 負債佔資產比率 

    FResult.loc[int(Number), '負債比_3Y'] = Data_File.loc[str("2019_" + Number), "負債比"] + Data_File.loc[str("2020_" + Number), "負債比"] + Data_File.loc[str("2021_" + Number), "負債比"]
    FResult.loc[int(Number), '負債比_3Y'] = FResult.loc[int(Number), '負債比_3Y'] / 3
    FResult.loc[int(Number), '負債比_3Y']  = round(FResult.loc[int(Number), '負債比_3Y'], 2)

    # ▌▌▌▌▌▌ ◎ 資產報酬率(ROA)  (未確認)
    
    FResult.loc[int(Number), 'ROA_3Y'] = Data_File.loc[str("2019_" + Number), "ROA"] + Data_File.loc[str("2020_" + Number), "ROA"] + Data_File.loc[str("2021_" + Number), "ROA"]
    FResult.loc[int(Number), 'ROA_3Y'] = FResult.loc[int(Number), 'ROA_3Y'] / 3
    FResult.loc[int(Number), 'ROA_3Y']  = round(FResult.loc[int(Number), 'ROA_3Y'], 2)

    # ▌▌▌▌▌▌ ◎ 股東權益報酬率(ROE)

    FResult.loc[int(Number), 'ROE_3Y'] = Data_File.loc[str("2019_" + Number), "ROE"] + Data_File.loc[str("2020_" + Number), "ROE"] + Data_File.loc[str("2021_" + Number), "ROE"]
    FResult.loc[int(Number), 'ROE_3Y'] = FResult.loc[int(Number), 'ROE_3Y'] / 3
    FResult.loc[int(Number), 'ROE_3Y']  = round(FResult.loc[int(Number), 'ROE_3Y'], 2)

    # ▌▌▌▌▌▌ ◎  毛利率

    FResult.loc[int(Number), '毛利率_3Y'] = Data_File.loc[str("2019_" + Number), "毛利率"] + Data_File.loc[str("2020_" + Number), "毛利率"] + Data_File.loc[str("2021_" + Number), "毛利率"]
    FResult.loc[int(Number), '毛利率_3Y'] = FResult.loc[int(Number), '毛利率_3Y'] / 3
    FResult.loc[int(Number), '毛利率_3Y']  = round(FResult.loc[int(Number), '毛利率_3Y'], 2)

    FResult.dropna(axis=0, how='any', inplace=True)

    FResult.to_csv(Path + "Result_3Y.csv", encoding="utf_8_sig")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌

'''
def GetDB():

    conn = sqlite3.connect("Finance.db")

    df = pd.read_csv("C:\\Senior Project\\" + 'Result_Y.csv', encoding="utf-8-sig") 
            
    df.to_sql("Result_Y", conn, if_exists="append", index=False)

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌
'''