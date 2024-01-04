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


def Get_Finance(num, name, number, season, seasons):

    Path = "C:\\Senior Project\\"

    Data_File = pd.read_csv(Path + "Finance.csv", index_col="代碼", encoding="utf_8_sig")

    # ▌▌▌▌▌▌ ◎ 流動比率  

    Current_Assets = Data_File.loc[season + "_" + number, "流動資產合計"]

    Current_Liabilities = Data_File.loc[season + "_" + number, "流動負債合計"]

    Current_Ratio = float(Current_Assets) / float(Current_Liabilities)

    Data_File.loc[season + "_" + number, "流動比率"] = Current_Ratio
    Data_File.loc[season + "_" + number, "流動比率"] = round(Data_File.loc[season + "_" + number, "流動比率"]*100, 2)
    
   
    # ▌▌▌▌▌▌ ◎ 速動比率  

    Current_Inventories = Data_File.loc[season + "_" + number, "存貨合計"]

    Quick_Ratio = ( float(Current_Assets) - float(Current_Inventories) ) / float(Current_Liabilities)

    Data_File.loc[season + "_" + number, "速動比率"] = Quick_Ratio
    Data_File.loc[season + "_" + number, "速動比率"] = round(Data_File.loc[season + "_" + number, "速動比率"]*100, 2)

    # ▌▌▌▌▌▌ ◎ 利息保障倍數 

    Interest_Expense = Data_File.loc[season + "_" + number, "利息費用"]
    Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]
        
    TIER = ( float(Profit_Btax) + float(Interest_Expense) ) / float(Interest_Expense)
    
    Data_File.loc[season + "_" + number, "利息保障倍數"] = TIER
    Data_File.loc[season + "_" + number, "利息保障倍數"] = round(Data_File.loc[season + "_" + number, "利息保障倍數"], 2)

    # ▌▌▌▌▌▌ ◎ 負債佔資產比率 

    Total_Assets = Data_File.loc[season + "_" + number, "資產總計"]

    Total_Liabilities = Data_File.loc[season + "_" + number, "負債總計"]
  
    Debt_Ratio = float(Total_Liabilities) / float(Total_Assets)

    Data_File.loc[season + "_" + number, "負債比"] = Debt_Ratio
    Data_File.loc[season + "_" + number, "負債比"] = round(Data_File.loc[season + "_" + number, "負債比"]*100, 2)

    # ▌▌▌▌▌▌ ◎ 稅後淨利率 = 純益率

    Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]

    Operating_Revenue = Data_File.loc[season + "_" + number, "營業收入合計"]

    Profit_Margin = float(Income_Net) / float(Operating_Revenue)

    Data_File.loc[season + "_" + number, "稅後淨利率"] = Profit_Margin
    Data_File.loc[season + "_" + number, "稅後淨利率"] = round(Data_File.loc[season + "_" + number, "稅後淨利率"]*100, 2)

    # ▌▌▌▌▌▌ ◎ 存貨週轉率  

    Current_Inventories = Data_File.loc[seasons[num] + "_" + number, "存貨合計"]
    Current_LInventories = Data_File.loc[seasons[num-1] + "_" + number, "存貨合計"]

    Operating_Costs = Data_File.loc[season + "_" + number, "營業成本合計"]

    Average_Inventories = (float(Current_Inventories) + float(Current_LInventories)) / 2
        
    Inventory_Turnover = float(Operating_Costs) / float(Average_Inventories)
    
    Data_File.loc[season + "_" + number, "存貨週轉率"] = Inventory_Turnover
    Data_File.loc[season + "_" + number, "存貨週轉率"] = round(Data_File.loc[season + "_" + number, "存貨週轉率"], 2)

    # ▌▌▌▌▌▌ ◎ 資產報酬率(ROA)  (未確認)

    Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]
    Interest_Expense = Data_File.loc[seasons[num]  + "_" + number, "利息費用"]

    Income_Tte = Data_File.loc[season + "_" + number, "所得稅費用"]
    Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]
    
    Total_Assets = Data_File.loc[seasons[num] + "_" + number, "資產總計"]
    Total_LAssets = Data_File.loc[seasons[num-1] + "_" + number, "資產總計"]

    Tax_Rate = round((float(Income_Tte) / float(Profit_Btax)),4)
    Average_Assets = (float(Total_Assets) + float(Total_LAssets)) / 2

    Total_ROA = (float(Income_Net) + float(Interest_Expense) * (1 - Tax_Rate))

    ROA = float(Total_ROA) / float(Average_Assets)   

    Data_File.loc[season + "_" + number, "ROA"] = ROA
    Data_File.loc[season + "_" + number, "ROA"] = round(Data_File.loc[season + "_" + number, "ROA"]*100, 2)

    # ▌▌▌▌▌▌ ◎ 股東權益報酬率(ROE)

    Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]

    Total_Equity = Data_File.loc[season + "_" + number, "權益總計"]
    Total_LEquity = Data_File.loc[seasons[num-1] + "_" + number, "權益總計"]

    Average_Equity = (float(Total_Equity) + float(Total_LEquity)) / 2

    ROE = float(Income_Net) / float(Average_Equity)

    Data_File.loc[season + "_" + number, "ROE"] = ROE
    Data_File.loc[season + "_" + number, "ROE"] = round(Data_File.loc[season + "_" + number, "ROE"]*100, 2)


    # ▌▌▌▌▌▌ ◎  毛利率

    Operating_Costs = Data_File.loc[season + "_" + number, "營業成本合計"]
    Operating_Revenue = Data_File.loc[season + "_" + number, "營業收入合計"]
    
    Gross_Margin =  ((float(Operating_Revenue) - float(Operating_Costs)) / float(Operating_Revenue))

    Data_File.loc[season + "_" + number, "毛利率"] = Gross_Margin
    Data_File.loc[season + "_" + number, "毛利率"] = round(Data_File.loc[season + "_" + number, "毛利率"]*100, 2)

    #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

    with open("C:\\Senior Project\\" + 'Result_Y.csv', 'a+', newline="", encoding='utf-8-sig') as File:
              
        writer = csv.writer(File)

        with open("C:\\Senior Project\\" + 'Result_Y.csv', 'r', newline="", encoding='utf-8-sig') as File:
            
            render = csv.reader(File)

            if not [row for row in render]:

                writer.writerow(("會計項目", "流動比率", "速動比率", "利息保障倍數", "毛利率", "存貨週轉率", "負債比", "稅後淨利率", "ROE", "ROA", "股票代碼", "股票名稱", "股票類別"))
                writer.writerow((Data_File.loc[season + "_" + number, "會計項目"][0:4], Data_File.loc[season + "_" + number, "流動比率"], Data_File.loc[season + "_" + number, "速動比率"], Data_File.loc[season + "_" + number, "利息保障倍數"], Data_File.loc[season + "_" + number, "毛利率"], Data_File.loc[season + "_" + number, "存貨週轉率"], Data_File.loc[season + "_" + number, "負債比"], Data_File.loc[season + "_" + number, "稅後淨利率"], Data_File.loc[season + "_" + number, "ROE"], Data_File.loc[season + "_" + number, "ROA"],Data_File.loc[season + "_" + number, "股票代碼"], Data_File.loc[season + "_" + number, "股票名稱"], Data_File.loc[season + "_" + number, "股票類別"]))
            else:
                writer.writerow((Data_File.loc[season + "_" + number, "會計項目"][0:4], Data_File.loc[season + "_" + number, "流動比率"], Data_File.loc[season + "_" + number, "速動比率"], Data_File.loc[season + "_" + number, "利息保障倍數"], Data_File.loc[season + "_" + number, "毛利率"], Data_File.loc[season + "_" + number, "存貨週轉率"], Data_File.loc[season + "_" + number, "負債比"], Data_File.loc[season + "_" + number, "稅後淨利率"], Data_File.loc[season + "_" + number, "ROE"], Data_File.loc[season + "_" + number, "ROA"],Data_File.loc[season + "_" + number, "股票代碼"], Data_File.loc[season + "_" + number, "股票名稱"], Data_File.loc[season + "_" + number, "股票類別"]))

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def GetDB():

    conn = sqlite3.connect("C:\\Senior Project\\Finance.db")

    df = pd.read_csv("C:\\Senior Project\\" + 'Result_Y.csv', encoding="utf-8-sig") 
            
    df.to_sql("Result_Y", conn, if_exists="append", index=False)

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌
